"""
Checkers GUI — Professional Edition
Dark slate theme · Rounded corners · Analytics dashboard · Move history
"""

import tkinter as tk
from tkinter import scrolledtext
import time
from GameBoard import GameBoard
from OtherStuff import WHITE, BLACK, BOARD_SIZE, WHITE_KING, BLACK_KING, EMPTY
from SearchToolBox import MinimaxSearch, AlphaBetaSearch, AlphaBetaWithOrdering
 

THEME = {
 
    'bg':            '#1B1B2F',
    'card':          '#252540',
    'card_alt':      '#2E2E4A',
    'border':        '#3A3A55',
 
    'sq_dark':       '#6B3A2A',
    'sq_light':      '#C9A86C',
    'sq_border':     '#4A2A1A',
    'coord':         '#8B8B9B',
 
    'piece_white':   '#F0EAD6',
    'piece_white_in':'#FFFAF0',
    'piece_black':   '#1A1A1A',
    'piece_black_in':'#333333',
    'piece_shadow':  '#4A2A1A',
    'piece_ring_w':  '#BFA66A',
    'piece_ring_b':  '#7A7A8A',
 
    'sel_glow':      '#FFB703',
    'jump':          '#E94560',
    'jump_ring':     '#B8001F',
    'move':          '#00ADB5',
    'move_ring':     '#007A80',
 
    'accent':        '#00ADB5',
    'accent_hover':  '#00CED1',
    'gold':          '#FFB703',
    'red':           '#E94560',
    'green':         '#2ECC71',
 
    'text':          '#EEEEEE',
    'text_dim':      '#9B9BB0',
    'text_muted':    '#6B6B80',
}

FONT_TITLE  = ('Segoe UI', 18, 'bold')
FONT_HEADER = ('Segoe UI', 13, 'bold')
FONT_BODY   = ('Segoe UI', 11)
FONT_SMALL  = ('Segoe UI', 9)
FONT_MONO   = ('Cascadia Code', 9)
FONT_PIECE  = ('Segoe UI Symbol', 22, 'bold')
 

def rounded_rect(canvas, x1, y1, x2, y2, r=12, **kw):
    """Draw a rounded rectangle on *canvas* using smooth polygon."""
    pts = [
        x1+r, y1,   x2-r, y1,   x2, y1,   x2, y1+r,
        x2, y2-r,   x2, y2,   x2-r, y2,
        x1+r, y2,   x1, y2,   x1, y2-r,
        x1, y1+r,   x1, y1,
    ]
    return canvas.create_polygon(pts, smooth=True, **kw)
 

class CheckerGUI:

    def __init__(self, ai_enabled=False, ai_strategy='AlphaBetaOrdering',
                 ai_depth=7, ai_time_limit=3.0):
 
        self.root = tk.Tk()
        mode = "Human vs AI" if ai_enabled else "Human vs Human"
        self.root.title(f"Checkers  —  {mode}")
        self.root.configure(bg=THEME['bg'])
        self.root.resizable(False, False)
 
        self.sq = 64
        self.margin = 24
        self.board_px = BOARD_SIZE * self.sq
        self.canvas_w = self.board_px + 2 * self.margin
        self.canvas_h = self.board_px + 2 * self.margin
 
        self.game_board = GameBoard()
        self.current_player = WHITE
        self.selected_pos = None
        self.valid_moves = []
        self.game_over = False
        self.must_continue_jumping = False
        self.move_counter = 0
 
        self.ai_enabled = ai_enabled
        self.ai_player = BLACK
        self.ai_depth = ai_depth
        self.ai_time_limit = ai_time_limit
        if ai_enabled:
            strategies = {
                'Minimax':            MinimaxSearch,
                'AlphaBeta':          AlphaBetaSearch,
                'AlphaBetaOrdering':  AlphaBetaWithOrdering,
            }
            cls = strategies.get(ai_strategy, AlphaBetaWithOrdering)
            self.ai_search = cls(ai_depth, ai_time_limit)
            self.ai_strategy_name = ai_strategy
 
        self._build_ui()
        self.draw_board()
        self.root.mainloop()
 
 
 

    def _build_ui(self):
 
        top = tk.Frame(self.root, bg=THEME['bg'])
        top.pack(fill=tk.BOTH, expand=True, padx=14, pady=14)
 
        left = tk.Frame(top, bg=THEME['bg'])
        left.pack(side=tk.LEFT, fill=tk.BOTH)

        self._build_header(left)
        self._build_board(left)
        self._build_status_bar(left)
 
        right = tk.Frame(top, bg=THEME['bg'], width=330)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(14, 0))
        right.pack_propagate(False)

        if self.ai_enabled:
            self._build_analytics_panel(right)
        self._build_history_panel(right)
        self._build_new_game_btn(right)
 

    def _build_header(self, parent):
        bar = tk.Canvas(parent, height=56, bg=THEME['bg'], highlightthickness=0)
        bar.pack(fill=tk.X, pady=(0, 10))
        bar.update_idletasks()
        w = max(bar.winfo_width(), self.canvas_w)
        rounded_rect(bar, 0, 0, w, 54, r=14,
                     fill=THEME['card'], outline=THEME['border'], width=1)
        bar.create_text(18, 27, anchor='w', text='CHECKERS',
                        font=FONT_TITLE, fill=THEME['gold'])

        self._turn_canvas = bar
        self._turn_text_id = bar.create_text(
            w - 18, 27, anchor='e', text="WHITE'S TURN",
            font=FONT_HEADER, fill=THEME['text'])

    def _set_turn_text(self, txt, color=None):
        self._turn_canvas.itemconfig(
            self._turn_text_id, text=txt, fill=color or THEME['text'])
 

    def _build_board(self, parent):
        frame = tk.Frame(parent, bg=THEME['bg'])
        frame.pack()
        self.canvas = tk.Canvas(frame,
                                width=self.canvas_w, height=self.canvas_h,
                                bg=THEME['bg'], highlightthickness=0)
        self.canvas.pack()
        self.canvas.bind('<Button-1>', self.on_canvas_click)
 

    def _build_status_bar(self, parent):
        self.status_var = tk.StringVar(value='Select a piece to move')
        bar = tk.Canvas(parent, height=40, bg=THEME['bg'], highlightthickness=0)
        bar.pack(fill=tk.X, pady=(10, 0))
        bar.update_idletasks()
        w = max(bar.winfo_width(), self.canvas_w)
        rounded_rect(bar, 0, 0, w, 38, r=10,
                     fill=THEME['card'], outline=THEME['border'], width=1)
        self._status_canvas = bar
        self._status_text_id = bar.create_text(
            w // 2, 19, text=self.status_var.get(),
            font=FONT_BODY, fill=THEME['text_dim'])
 
        def _sync(*_):
            bar.itemconfig(self._status_text_id, text=self.status_var.get())
        self.status_var.trace_add('write', _sync)
 

    def _build_analytics_panel(self, parent):
        outer = tk.Canvas(parent, bg=THEME['bg'], highlightthickness=0, height=230)
        outer.pack(fill=tk.X, pady=(0, 10))
        outer.update_idletasks()
 
        def _draw_analytics(_event=None):
            outer.delete('all')
            w = outer.winfo_width() or 320
            rounded_rect(outer, 0, 0, w, 228, r=14,
                         fill=THEME['card'], outline=THEME['border'])
 
            outer.create_text(16, 20, anchor='w', text='AI  ANALYTICS',
                              font=FONT_HEADER, fill=THEME['gold'])
 
            y = 48
            for label, val in [('Strategy', self.ai_strategy_name),
                               ('Max depth', str(self.ai_depth)),
                               ('Time limit', f'{self.ai_time_limit}s')]:
                outer.create_text(20, y, anchor='w', text=label,
                                  font=FONT_SMALL, fill=THEME['text_muted'])
                outer.create_text(w - 20, y, anchor='e', text=val,
                                  font=('Segoe UI', 9, 'bold'), fill=THEME['text'])
                y += 20
 
            outer.create_line(16, y + 4, w - 16, y + 4,
                              fill=THEME['border'], width=1)
            y += 16

            outer.create_text(16, y, anchor='w', text='Last Move Stats',
                              font=('Segoe UI', 10, 'bold'), fill=THEME['accent'])
            y += 24
 
            self.analytics_labels = {}
            metrics = [
                ('Nodes expanded', 'nodes', THEME['green']),
                ('Nodes pruned',   'prunes', THEME['gold']),
                ('Depth reached',  'depth',  THEME['accent']),
                ('Time elapsed',   'time',   THEME['red']),
            ]
            for label, key, color in metrics:
                outer.create_text(20, y, anchor='w', text=label,
                                  font=FONT_SMALL, fill=THEME['text_dim'])
                tid = outer.create_text(w - 20, y, anchor='e', text='—',
                                        font=('Segoe UI', 9, 'bold'), fill=color)
                self.analytics_labels[key] = tid
                y += 22

        self._analytics_canvas = outer
        self._draw_analytics = _draw_analytics
        outer.bind('<Configure>', _draw_analytics)
        _draw_analytics()
 

    def _build_history_panel(self, parent):
 
        wrapper = tk.Frame(parent, bg=THEME['card'], bd=0, relief=tk.FLAT)
        wrapper.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
 
        hdr = tk.Canvas(wrapper, height=36, bg=THEME['card'], highlightthickness=0)
        hdr.pack(fill=tk.X)
        hdr.update_idletasks()
        hdr.create_text(16, 18, anchor='w', text='MOVE  HISTORY',
                        font=FONT_HEADER, fill=THEME['gold'])

        self.history_text = scrolledtext.ScrolledText(
            wrapper, font=FONT_MONO,
            bg=THEME['bg'], fg=THEME['text'],
            insertbackground=THEME['text'],
            selectbackground=THEME['accent'],
            relief=tk.FLAT, padx=10, pady=8,
            wrap=tk.WORD, state='disabled', bd=0)
        self.history_text.pack(fill=tk.BOTH, expand=True, padx=6, pady=(0, 6))
 
        self.history_text.tag_config('white_mv', foreground=THEME['piece_white'],
                                     font=(FONT_MONO[0], 9, 'bold'))
        self.history_text.tag_config('black_mv', foreground=THEME['accent'],
                                     font=(FONT_MONO[0], 9, 'bold'))
        self.history_text.tag_config('jump', foreground=THEME['red'],
                                     font=(FONT_MONO[0], 9, 'bold'))
        self.history_text.tag_config('king', foreground=THEME['gold'],
                                     font=(FONT_MONO[0], 9, 'bold'))
        self.history_text.tag_config('info', foreground=THEME['text_muted'],
                                     font=(FONT_MONO[0], 9, 'italic'))

        self._write_history_header()

    def _write_history_header(self):
        self.history_text.config(state='normal')
        self.history_text.delete('1.0', tk.END)
        self.history_text.insert(tk.END, '  Game started\n', 'info')
        self.history_text.insert(tk.END, '  ─' * 12 + '\n', 'info')
        self.history_text.config(state='disabled')
 

    def _build_new_game_btn(self, parent):
        btn = tk.Button(parent, text='NEW  GAME',
                        font=FONT_HEADER, fg='#FFFFFF',
                        bg=THEME['accent'], activebackground=THEME['accent_hover'],
                        activeforeground='#FFFFFF',
                        relief=tk.FLAT, bd=0, padx=22, pady=10,
                        cursor='hand2', command=self.new_game)
        btn.pack(fill=tk.X)
 
 
 

    def draw_board(self):
        c = self.canvas
        c.delete('all')
        m = self.margin
        sq = self.sq
        bpx = self.board_px
 
        rounded_rect(c, m - 6, m - 6, m + bpx + 6, m + bpx + 6, r=10,
                     fill=THEME['sq_border'], outline=THEME['sq_border'])
 
        for r in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x1 = m + col * sq
                y1 = m + r * sq
                color = THEME['sq_dark'] if (r + col) % 2 else THEME['sq_light']
                c.create_rectangle(x1, y1, x1 + sq, y1 + sq,
                                   fill=color, outline=THEME['sq_border'], width=1)
 
        for i in range(BOARD_SIZE):
 
            c.create_text(m // 2, m + i * sq + sq // 2,
                          text=str(i + 1), font=FONT_SMALL, fill=THEME['coord'])
 
            c.create_text(m + i * sq + sq // 2, m + bpx + m // 2,
                          text=chr(ord('a') + i), font=FONT_SMALL, fill=THEME['coord'])
 
        if self.selected_pos:
            sr, sc = self.selected_pos
            x1 = m + sc * sq
            y1 = m + sr * sq
            c.create_rectangle(x1 + 1, y1 + 1, x1 + sq - 1, y1 + sq - 1,
                               outline=THEME['sel_glow'], width=3)
 
        if self.selected_pos:
            fr, fc = self.selected_pos
            for tr, tc in self.valid_moves:
                xc = m + tc * sq + sq // 2
                yc = m + tr * sq + sq // 2
                is_jump = abs(tr - fr) == 2
                if is_jump:
                    c.create_oval(xc - 20, yc - 20, xc + 20, yc + 20,
                                  fill=THEME['jump'], outline=THEME['jump_ring'], width=2)
                    c.create_text(xc, yc, text='×', font=('Segoe UI', 16, 'bold'),
                                  fill='#FFFFFF')
                else:
                    c.create_oval(xc - 14, yc - 14, xc + 14, yc + 14,
                                  fill=THEME['move'], outline=THEME['move_ring'], width=2)
 
        self._draw_pieces()

    def _draw_pieces(self):
        c = self.canvas
        m = self.margin
        sq = self.sq

        for r in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.game_board.board[r][col]
                if piece == EMPTY:
                    continue

                xc = m + col * sq + sq // 2
                yc = m + r * sq + sq // 2
                rad = sq // 2 - 6
 
                off = 3
                c.create_oval(xc - rad + off, yc - rad + off,
                              xc + rad + off, yc + rad + off,
                              fill=THEME['piece_shadow'], outline='')

                if piece in (WHITE, WHITE_KING):
                    fill, inner, ring = (THEME['piece_white'],
                                         THEME['piece_white_in'],
                                         THEME['piece_ring_w'])
                else:
                    fill, inner, ring = (THEME['piece_black'],
                                         THEME['piece_black_in'],
                                         THEME['piece_ring_b'])
 
                c.create_oval(xc - rad, yc - rad, xc + rad, yc + rad,
                              fill=fill, outline=ring, width=3)
 
                c.create_oval(xc - rad + 7, yc - rad + 7,
                              xc + rad - 7, yc + rad - 7,
                              fill=inner, outline='')
 
                if piece == WHITE_KING:
                    c.create_text(xc, yc + 1, text='♔',
                                  font=FONT_PIECE, fill=THEME['gold'])
                elif piece == BLACK_KING:
                    c.create_text(xc, yc + 1, text='♚',
                                  font=FONT_PIECE, fill=THEME['piece_ring_b'])
 
 
 

    def new_game(self):
        self.game_board = GameBoard()
        self.current_player = WHITE
        self.selected_pos = None
        self.valid_moves = []
        self.game_over = False
        self.must_continue_jumping = False
        self.move_counter = 0
        self.status_var.set('Select a piece to move')
        self._set_turn_text("WHITE'S TURN")
        self._write_history_header()
        if self.ai_enabled and hasattr(self, 'analytics_labels'):
            for tid in self.analytics_labels.values():
                self._analytics_canvas.itemconfig(tid, text='—')
        self.draw_board()

    def get_valid_moves(self, row, col):
        piece = self.game_board.board[row][col]
        if piece not in [self.current_player, self.current_player.lower()]:
            return []
        moves = []
        for dr, dc in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
            tr, tc = row + dr, col + dc
            if 0 <= tr < BOARD_SIZE and 0 <= tc < BOARD_SIZE:
                if self.game_board.is_valid_move(row, col, tr, tc, self.current_player):
                    moves.append((tr, tc))
        for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            tr, tc = row + dr, col + dc
            if 0 <= tr < BOARD_SIZE and 0 <= tc < BOARD_SIZE:
                if self.game_board.is_valid_move(row, col, tr, tc, self.current_player):
                    moves.append((tr, tc))
        return moves
 

    def add_move_to_history(self, player, start, end, was_jump, promoted, is_ai=False):
        self.move_counter += 1
        h = self.history_text
        h.config(state='normal')
        tag = 'white_mv' if player == WHITE else 'black_mv'
        icon = '○' if player == WHITE else '●'
        ai_tag = ' AI' if is_ai else ''
        h.insert(tk.END, f' {self.move_counter:>3}. {icon}{ai_tag} ', tag)
        h.insert(tk.END,
                 f'({start[0]+1},{start[1]+1})→({end[0]+1},{end[1]+1})')
        if was_jump:
            h.insert(tk.END, '  ✕capture', 'jump')
        if promoted:
            h.insert(tk.END, '  ★king', 'king')
        h.insert(tk.END, '\n')
        h.config(state='disabled')
        h.see(tk.END)
 

    def update_analytics_display(self, analytics):
        if not self.ai_enabled or not hasattr(self, 'analytics_labels'):
            return
        ac = self._analytics_canvas
        ac.itemconfig(self.analytics_labels['nodes'],
                      text=f'{analytics.NumberNodesExpanded:,}')
        ac.itemconfig(self.analytics_labels['prunes'],
                      text=f'{analytics.NumberNodesPruned:,}')
        ac.itemconfig(self.analytics_labels['depth'],
                      text=f'{analytics.MaxDepthReached}')
        elapsed = analytics.GetTimeElapsed() if hasattr(analytics, 'GetTimeElapsed') else 0
        ac.itemconfig(self.analytics_labels['time'],
                      text=f'{elapsed:.3f}s')
 

    def check_game_over(self):
        white_n = sum(1 for row in self.game_board.board
                      for cell in row if cell.upper() == WHITE)
        black_n = sum(1 for row in self.game_board.board
                      for cell in row if cell.upper() == BLACK)

        winner = None
        if white_n == 0:
            winner = 'BLACK'
        elif black_n == 0:
            winner = 'WHITE'
        elif not self.game_board.has_any_legal_move(self.current_player):
            winner = 'BLACK' if self.current_player == WHITE else 'WHITE'

        if winner:
            self.game_over = True
            self.status_var.set(f'{winner} WINS!')
            self._set_turn_text(f'GAME OVER — {winner} WINS!', THEME['gold'])
            h = self.history_text
            h.config(state='normal')
            h.insert(tk.END, '\n  ─' * 12 + '\n', 'info')
            tag = 'white_mv' if winner == 'WHITE' else 'black_mv'
            h.insert(tk.END, f'  {winner} WINS!\n', tag)
            h.config(state='disabled')
            h.see(tk.END)
            return True
        return False
 

    def on_canvas_click(self, event):
        if self.game_over:
            return
        m = self.margin
        col = (event.x - m) // self.sq
        row = (event.y - m) // self.sq
        if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
            return

        piece = self.game_board.board[row][col]
 
        if self.must_continue_jumping and self.selected_pos:
            fr, fc = self.selected_pos
            if (row, col) in self.valid_moves:
                result = self.game_board.make_move(fr, fc, row, col,
                                                   self.current_player)
                self.add_move_to_history(self.current_player, (fr, fc),
                                         (row, col), result['was_jump'],
                                         result['promoted'], False)
                jumps = [(r, c) for r, c in self.get_valid_moves(row, col)
                         if abs(r - row) == 2]
                if jumps:
                    self.selected_pos = (row, col)
                    self.valid_moves = jumps
                    self.must_continue_jumping = True
                    self.status_var.set(
                        f'Continue jumping! ({len(jumps)} available)')
                else:
                    self.status_var.set('Multi-jump complete')
                    self.selected_pos = None
                    self.valid_moves = []
                    self.must_continue_jumping = False
                    if not self.check_game_over():
                        self.switch_turn()
                self.draw_board()
            return
 
        if piece in [self.current_player, self.current_player.lower()]:
            self.selected_pos = (row, col)
            self.valid_moves = self.get_valid_moves(row, col)
            j = sum(1 for r, c in self.valid_moves if abs(r - row) == 2)
            n = len(self.valid_moves) - j
            self.status_var.set(f'{j} jump(s)  ·  {n} move(s)')
            self.draw_board()
            return
 
        if self.selected_pos:
            fr, fc = self.selected_pos
            if (row, col) in self.valid_moves:
                result = self.game_board.make_move(fr, fc, row, col,
                                                   self.current_player)
                is_jump = abs(row - fr) == 2
                self.add_move_to_history(self.current_player, (fr, fc),
                                         (row, col), result['was_jump'],
                                         result['promoted'], False)
                if is_jump:
                    jumps = [(r, c) for r, c in self.get_valid_moves(row, col)
                             if abs(r - row) == 2]
                    if jumps:
                        self.selected_pos = (row, col)
                        self.valid_moves = jumps
                        self.must_continue_jumping = True
                        self.status_var.set(
                            f'Must continue jump! ({len(jumps)} available)')
                        self.draw_board()
                        return

                self.status_var.set('Move complete')
                self.selected_pos = None
                self.valid_moves = []
                self.must_continue_jumping = False
                if not self.check_game_over():
                    self.switch_turn()
                self.draw_board()
            else:
                self.status_var.set('Invalid — click a highlighted square')
 

    def switch_turn(self):
        self.current_player = BLACK if self.current_player == WHITE else WHITE
        if self.ai_enabled and self.current_player == self.ai_player:
            self._set_turn_text('AI  THINKING …', THEME['red'])
            self.status_var.set(f'AI thinking ({self.ai_strategy_name}) …')
            self.root.after(100, self.make_ai_move)
        else:
            who = 'WHITE' if self.current_player == WHITE else 'BLACK'
            self._set_turn_text(f"{who}'S TURN")
            self.status_var.set('Select a piece to move')

    def make_ai_move(self):
        if self.game_over:
            return
        self.root.update()

        best_move = self.ai_search.GetBestMove(self.game_board,
                                                self.current_player)
        if best_move is None:
            self.status_var.set('AI has no legal moves')
            self.check_game_over()
            return

        sr, sc = best_move.StartingMoveLocation
        tr, tc = best_move.DestinationLocation
        result = self.game_board.make_move(sr, sc, tr, tc,
                                           self.current_player)

        self.add_move_to_history(self.current_player, (sr, sc), (tr, tc),
                                 result['was_jump'], result['promoted'], True)

        if hasattr(self.ai_search, 'Analytics'):
            self.update_analytics_display(self.ai_search.Analytics)

        desc = f'AI  ({sr+1},{sc+1}) → ({tr+1},{tc+1})'
        if result['was_jump']:
            desc += '  ✕capture'
        if result['promoted']:
            desc += '  ★king'
        self.status_var.set(desc)
        self.draw_board()

        if not self.check_game_over():
            self.switch_turn()
 

if __name__ == '__main__':
    CheckerGUI()
