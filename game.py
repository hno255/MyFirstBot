import discord
from discord.ui import View, Button
from typing import Optional

class TicTacToe:
    """Handles the game logic for Tic Tac Toe"""
    
    def __init__(self):
        self.board = [' ' for _ in range(9)]  # 3x3 board
        self.current_player = 'X'  # X always starts
        self.game_over = False
        self.winner = None
    
    def make_move(self, position: int) -> bool:
        """
        Make a move at the given position (0-8)
        Returns True if move was valid, False otherwise
        """
        if position < 0 or position > 8:
            return False
        
        if self.board[position] != ' ':
            return False
        
        self.board[position] = self.current_player
        self.check_game_state()
        
        # Switch player
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        return True
    
    def check_game_state(self):
        """Check if the game is won or if it's a draw"""
        # Winning combinations
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]
        
        for combo in winning_combinations:
            if (self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ' '):
                self.game_over = True
                self.winner = self.board[combo[0]]
                return
        
        # Check for draw
        if ' ' not in self.board:
            self.game_over = True
            self.winner = 'Draw'
    
    def display_board(self) -> str:
        """Display the board in a readable format"""
        board_str = ""
        for i in range(3):
            for j in range(3):
                piece = self.board[i * 3 + j]
                piece = piece if piece != ' ' else str(i * 3 + j)
                board_str += f"[{piece}]"
            board_str += "\n"
        return board_str
    
    def is_valid_move(self, position: int) -> bool:
        """Check if a position is a valid move"""
        return 0 <= position <= 8 and self.board[position] == ' '


class TicTacToeButton(Button):
    """Custom button for Tic Tac Toe board"""
    
    def __init__(self, position: int, game: TicTacToe):
        super().__init__(style=discord.ButtonStyle.secondary, label=" ", row=position // 3)
        self.position = position
        self.game = game
    
    async def callback(self, interaction: discord.Interaction):
        # This will be handled by TicTacToeView
        await interaction.response.defer()


class TicTacToeView(View):
    """View that manages the Tic Tac Toe game"""
    
    def __init__(self, game: TicTacToe, player_x: discord.User, player_o: discord.User):
        super().__init__()
        self.game = game
        self.player_x = player_x
        self.player_o = player_o
        self.original_message = None
        
        # Create buttons for each position
        for i in range(9):
            button = TicTacToeButton(i, game)
            button.callback = self.create_button_callback(i)
            self.add_item(button)
    
    def create_button_callback(self, position: int):
        """Create a callback for a button at a specific position"""
        async def callback(interaction: discord.Interaction):
            # Check if it's the current player's turn
            current_player = self.player_x if self.game.current_player == 'X' else self.player_o
            
            if interaction.user.id != current_player.id:
                await interaction.response.send_message(
                    f"It's {current_player.mention}'s turn!", 
                    ephemeral=True
                )
                return
            
            # Try to make the move
            if not self.game.make_move(position):
                await interaction.response.send_message(
                    "That position is already taken!", 
                    ephemeral=True
                )
                return
            
            # Update button
            button = self.children[position]
            button.label = self.game.board[position]
            button.style = discord.ButtonStyle.success if button.label == 'X' else discord.ButtonStyle.danger
            button.disabled = True
            
            # Update the message
            embed = self.create_embed()
            
            # If game is over, disable all buttons
            if self.game.game_over:
                for item in self.children:
                    item.disabled = True
            
            await interaction.response.edit_message(embed=embed, view=self)
        
        return callback
    
    def create_embed(self) -> discord.Embed:
        """Create an embed showing the current game state"""
        if self.game.game_over:
            if self.game.winner == 'Draw':
                title = "Game Over - It's a Draw!"
                color = discord.Color.greyple()
                description = "The game ended in a draw."
            else:
                winner = self.player_x if self.game.winner == 'X' else self.player_o
                title = f"Game Over - {winner.name} Wins!"
                color = discord.Color.gold()
                description = f"{winner.mention} won the game!"
        else:
            current_player = self.player_x if self.game.current_player == 'X' else self.player_o
            title = "Tic Tac Toe"
            description = f"{self.player_x.mention} vs {self.player_o.mention}"
            color = discord.Color.blue()
        
        embed = discord.Embed(
            title=title,
            description=description,
            color=color
        )
        
        if not self.game.game_over:
            current_player = self.player_x if self.game.current_player == 'X' else self.player_o
            embed.add_field(
                name="Current Player",
                value=f"{current_player.mention} ({self.game.current_player})",
                inline=False
            )
        
        embed.add_field(name="Board", value=self.game.display_board(), inline=False)
        
        return embed
