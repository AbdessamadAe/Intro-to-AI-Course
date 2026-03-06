import tkinter as tk
from tkinter import ttk
#import GameBoard
#import PlayingTheGame
#from OtherStuff import WHITE, BLACK

class CheckerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Checkers: Play against a bot")
        self.root.geometry("1000x700")
        self.root.minsize(900, 600)
        self.square_size = 65 

        #Game state (mock for design)
        self.status_var = tk.StringVar(value="🟢 GUI Loading...")

        self.current_player = "W"
        self.selected_piece = None
        self.game_phase = "selecting" #selecting, moving, ai_thinking

        self.create_ui_layout()
        self.draw_board()
        self.root.mainloop()

    def create_ui_layout(self):
        #TOP HEADER
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill = tk.X, padx=15, pady=(15,10))
        ttk.Label(header_frame, text="🎯 CHECKERS GAME: PLAY AGAINST A BOT", font=("Arial", 20,"bold")).pack(side=tk.LEFT)

        self.turn_label = ttk.Label(header_frame, text= "👤 WHITE'S TURN", font=("Arial",15,"bold"))
        self.turn_label.pack(side=tk.RIGHT)

        #MAIN GAME AREA
        main_frame = ttk.Frame(self.root)
        main_frame.pack(expand = True, fill=tk.BOTH, padx=15, pady=8)

        #LEFT SIDE - Game board
        self.canvas = tk.Canvas(main_frame, width=520, height=520,bg="#deb887", relief = tk.RAISED, bd=2)
        self.canvas.pack(side=tk.LEFT, padx=(0,17))
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        #RIGHT SIDE - BOTTOM SIDE
        self.create_control_panel(main_frame)

        self.create_game_log()
    
    def draw_board(self):
        self.canvas.delete("all")
        for row in range(8):
            for col in range(8):
                x1, y1 = col*self.square_size, row*self.square_size
                color = "saddlebrown" if (row+col)%2 else "wheat"
                self.canvas.create_rectangle(x1, y1, x1+72, y1+72,fill = color, outline="brown")
    
        
    def create_control_panel(self, parent):
        frame = ttk.LabelFrame(parent, text="🎮 CONTROLS", padding=15)
        frame.pack(side=tk.RIGHT, fill=tk.Y)

        ttk.Button(frame, text="🚀 Test",command=self.test_click).pack(fill=tk.X, pady=5)

        ttk.Label(frame, textvariable=self.status_var, relief=tk.SUNKEN).pack(fill=tk.X, pady=5)

    def test_click(self):
        self.status_var.set("✅ Test button WORKS! 🎉")
        self.turn_label.config(text="🤖 Testing AI...")

    def on_canvas_click(self, event):
        col, row = event.x//self.square_size, event.y//self.square_size
        self.status_var.set(f"Clicked({row},{col})")
        self.log_message(f"Click: row {row}, col {col}")

    def create_game_log(self):
        # ✅ Simple log for now
        log_frame = ttk.LabelFrame(self.root, text="📝 Game Log", padding=10)
        log_frame.pack(fill=tk.X, padx=15, pady=(0,15))

        self.log_text = tk.Text(log_frame, height=8, wrap=tk.WORD, state=tk.DISABLED)
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.config(yscrollcommand=scrollbar.set)

        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,10))
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_message("🎮 Checkers started - Smaller board + bigger log!")
        self.log_message("🎮 Game started - Click board to test logging!")

    def log_message(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END,f"{message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)




    
if __name__ == "__main__":
    app = CheckerGUI()
        
                         




    
        
