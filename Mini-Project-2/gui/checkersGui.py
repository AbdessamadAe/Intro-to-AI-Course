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
        header_frame.pack(fill = tk.X, padx=20, pady=(20,10))
        ttk.Label(header_frame, text="🎯 CHECKERS GAME: PLAY AGAINST A BOT", font=("Arial", 22,"bold")).pack(side=tk.LEFT)

        self.turn_label = ttk.Label(header_frame, text= "👤 WHITE'S TURN", font=("Arial",16,"bold"))
        self.turn_label.pack(side=tk.RIGHT)

        #MAIN GAME AREA
        main_frame = ttk.Frame(self.root)
        main_frame.pack(expand = True, fill=tk.BOTH, padx=20, pady=10)

        #LEFT SIDE - Game board
        self.canvas = tk.Canvas(main_frame, width=576, height=576,bg="#deb887", relief = tk.RAISED, bd=3)
        self.canvas.pack(side=tk.LEFT, padx=(0,20))
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        #RIGHT SIDE - BOTTOM SIDE
        self.create_control_panel(main_frame)
        self.create_game_log()
    
    def draw_board(self):
        self.canvas.delete("all")
        for row in range(8):
            for col in range(8):
                x1, y1 = col*72, row*72
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
        col, row = event.x//72, event.y//72
        self.status_var.set(f"Clicked({row},{col})")

    def create_game_log(self):
        # ✅ Simple log for now
        log_frame = ttk.LabelFrame(self.root, text="📝 Game Log", padding=10)
        log_frame.pack(fill=tk.X, padx=20, pady=10)
        self.log_label = ttk.Label(log_frame, text="No moves yet...")
        self.log_label.pack()



    
if __name__ == "__main__":
    app = CheckerGUI()
        
                         




    
        
