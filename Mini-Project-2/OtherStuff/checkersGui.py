import tkinter as tk
from tkinter import scrolledtext
import time
from GameBoard import GameBoard
from OtherStuff import WHITE, BLACK, BOARD_SIZE, WHITE_KING, BLACK_KING, EMPTY
from SearchToolBox import MinimaxSearch, AlphaBetaSearch, AlphaBetaWithOrdering

# ── Fixed window dimensions (config screen and game screen share these) ──────
WIN_W = 940
WIN_H = 716

# ── Dark theme: black / charcoal / wood accents / off-white ─────────────────
T = {
    # surfaces
    'bg':          '#0E0B08',
    'card':        '#181210',
    'card_alt':    '#221A14',
    'border':      '#3A2A1E',
    'border_lt':   '#5A3E2A',
    # board
    'sq_dark':     '#2A1608',
    'sq_light':    '#8C6030',
    'sq_frame':    '#080503',
    'coord':       '#5A3E28',
    # pieces
    'pw':          '#EDE0C8',
    'pw_in':       '#F8F0E0',
    'pb':          '#0E0B08',
    'pb_in':       '#1A1410',
    'shadow':      '#050302',
    'ring_w':      '#B09060',
    'ring_b':      '#3A2A1A',
    # board markers
    'sel':         '#D4B880',
    'jump_fill':   '#2E1508',
    'jump_ring':   '#7A4820',
    'move_fill':   '#1E1208',
    'move_ring':   '#5A3818',
    # ui accent / buttons
    'accent':      '#A07840',
    'accent_h':    '#C09050',
    'btn_bg':      '#221A14',
    'btn_h':       '#2E2018',
    # text
    'text':        '#D8C8A8',
    'text_dim':    '#7A6448',
    'text_lo':     '#4A3828',
    'white':       '#F0E4C8',
    # value tiers (analytics / history)
    'val_a':       '#D8C8A8',
    'val_b':       '#A08060',
    'val_c':       '#6A5040',
}

FONT_TITLE  = ('Segoe UI', 22, 'bold')
FONT_HEADER = ('Segoe UI', 13, 'bold')
FONT_BODY   = ('Segoe UI', 11)
FONT_SMALL  = ('Segoe UI', 9)
FONT_MONO   = ('Cascadia Code', 9)


def _rounded(canvas, x1, y1, x2, y2, r=10, **kw):
    pts = [x1+r, y1, x2-r, y1, x2, y1, x2, y1+r,
           x2, y2-r, x2, y2, x2-r, y2, x1+r, y2,
           x1, y2, x1, y2-r, x1, y1+r, x1, y1]
    return canvas.create_polygon(pts, smooth=True, **kw)


def _center_window(root, w, h):
    root.update_idletasks()
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x  = (sw - w) // 2
    y  = (sh - h) // 2
    root.geometry(f'{w}x{h}+{x}+{y}')


# ─────────────────────────────────────────────────────────────────────────────
#  CONFIG SCREEN
# ─────────────────────────────────────────────────────────────────────────────
class ConfigScreen:

    def __init__(self):
        self.result = None
        self.root   = tk.Tk()
        self.root.title('Checkers')
        self.root.configure(bg=T['bg'])
        self.root.resizable(False, False)
        self.root.protocol('WM_DELETE_WINDOW', self._on_close)

        self._mode     = tk.StringVar(value='human')
        self._strategy = tk.StringVar(value='AlphaBetaOrdering')
        self._depth    = tk.IntVar(value=7)
        self._time     = tk.DoubleVar(value=3.0)

        _center_window(self.root, WIN_W, WIN_H)
        self._build()
        self.root.mainloop()

    # ── layout ────────────────────────────────────────────────────────────────
    def _build(self):
        # Full-window canvas so we can draw a background pattern / center card
        bg = tk.Canvas(self.root, width=WIN_W, height=WIN_H,
                       bg=T['bg'], highlightthickness=0)
        bg.place(x=0, y=0)

        # Subtle grid texture
        step = 40
        for x in range(0, WIN_W, step):
            bg.create_line(x, 0, x, WIN_H, fill=T['card_alt'], width=1)
        for y in range(0, WIN_H, step):
            bg.create_line(0, y, WIN_W, y, fill=T['card_alt'], width=1)

        # Center card dimensions
        cw, ch = 420, 560
        cx = (WIN_W - cw) // 2
        cy = (WIN_H - ch) // 2

        # Card shadow
        _rounded(bg, cx+4, cy+4, cx+cw+4, cy+ch+4, r=14,
                 fill='#000000', outline='')
        # Card body
        _rounded(bg, cx, cy, cx+cw, cy+ch, r=14,
                 fill=T['card'], outline=T['border'], width=1)
        # Top accent line
        bg.create_line(cx+14, cy+1, cx+cw-14, cy+1,
                       fill=T['border_lt'], width=1)

        # Title area
        bg.create_text(cx + cw//2, cy + 44,
                       text='CHECKERS', font=('Segoe UI', 28, 'bold'),
                       fill=T['white'])
        bg.create_text(cx + cw//2, cy + 74,
                       text='configure your game', font=('Segoe UI', 10),
                       fill=T['text_lo'])

        # Divider
        bg.create_line(cx+24, cy+94, cx+cw-24, cy+94, fill=T['border'], width=1)

        # All interactive widgets in a frame placed over the card
        form = tk.Frame(self.root, bg=T['card'], bd=0)
        form.place(x=cx + 24, y=cy + 106, width=cw - 48)

        self._build_form(form, cw - 48)

    def _build_form(self, parent, width):
        # ── Section: Game Mode ─────────────────────────────────────────────
        tk.Label(parent, text='GAME MODE', font=('Segoe UI', 8, 'bold'),
                 bg=T['card'], fg=T['text_lo']).pack(anchor='w', pady=(0, 6))

        mode_frame = tk.Frame(parent, bg=T['card_alt'], bd=0)
        mode_frame.pack(fill=tk.X, pady=(0, 16))
        for label, val in [('Human vs Human', 'human'),
                           ('Human vs AI   (you play White)', 'ai')]:
            rb = tk.Radiobutton(mode_frame, text=label, variable=self._mode, value=val,
                                command=self._toggle_ai,
                                font=FONT_BODY, bg=T['card_alt'], fg=T['text'],
                                selectcolor=T['bg'], activebackground=T['card_alt'],
                                activeforeground=T['white'],
                                indicatoron=True)
            rb.pack(anchor='w', padx=14, pady=7)

        # ── Section: AI Configuration ──────────────────────────────────────
        self._ai_lbl = tk.Label(parent, text='AI CONFIGURATION',
                                font=('Segoe UI', 8, 'bold'),
                                bg=T['card'], fg=T['text_lo'])
        self._ai_lbl.pack(anchor='w', pady=(0, 6))

        self._ai_card = tk.Frame(parent, bg=T['card_alt'], bd=0)

        tk.Label(self._ai_card, text='Search Strategy',
                 font=('Segoe UI', 9, 'bold'), bg=T['card_alt'],
                 fg=T['text_dim']).pack(anchor='w', padx=14, pady=(12, 4))

        for lbl, val in [('Minimax', 'Minimax'),
                         ('Alpha-Beta Pruning', 'AlphaBeta'),
                         ('Alpha-Beta + Move Ordering  (recommended)', 'AlphaBetaOrdering')]:
            tk.Radiobutton(self._ai_card, text=lbl, variable=self._strategy, value=val,
                           font=FONT_SMALL, bg=T['card_alt'], fg=T['text'],
                           selectcolor=T['bg'], activebackground=T['card_alt'],
                           activeforeground=T['white']).pack(anchor='w', padx=24, pady=2)

        tk.Frame(self._ai_card, bg=T['border'], height=1).pack(fill=tk.X, padx=14, pady=10)

        for lbl, var, frm, to, res, unit in [
            ('Search Depth',      self._depth, 5,   9,   1,   None),
            ('Time Limit (sec)',  self._time,  1.0, 3.0, 0.5, None),
        ]:
            row = tk.Frame(self._ai_card, bg=T['card_alt'])
            row.pack(fill=tk.X, padx=14, pady=(0, 4))
            tk.Label(row, text=lbl, font=('Segoe UI', 9, 'bold'),
                     bg=T['card_alt'], fg=T['text_dim']).pack(side=tk.LEFT)
            tk.Label(row, textvariable=var, width=4,
                     font=('Segoe UI', 10, 'bold'),
                     bg=T['card_alt'], fg=T['val_a']).pack(side=tk.RIGHT)
            tk.Scale(self._ai_card, variable=var, from_=frm, to=to, resolution=res,
                     orient=tk.HORIZONTAL, showvalue=False,
                     bg=T['card_alt'], fg=T['text'],
                     troughcolor=T['border'], activebackground=T['accent'],
                     highlightthickness=0, bd=0).pack(fill=tk.X, padx=14, pady=(0, 10))

        # ── Start button ───────────────────────────────────────────────────
        self._start_btn = tk.Button(
            parent, text='START  GAME',
            font=FONT_HEADER, fg=T['white'],
            bg=T['btn_bg'], activebackground=T['btn_h'],
            activeforeground=T['white'],
            relief=tk.FLAT, bd=0, padx=22, pady=13,
            cursor='hand2', command=self._start)
        self._start_btn.pack(fill=tk.X, pady=(14, 0))
        self._start_btn.bind('<Enter>', lambda _: self._start_btn.config(bg=T['btn_h']))
        self._start_btn.bind('<Leave>', lambda _: self._start_btn.config(bg=T['btn_bg']))

        self._toggle_ai()

    def _toggle_ai(self):
        if self._mode.get() == 'ai':
            self._ai_lbl.pack(anchor='w', pady=(0, 6))
            self._ai_card.pack(fill=tk.X, pady=(0, 16))
        else:
            self._ai_lbl.pack_forget()
            self._ai_card.pack_forget()

    def _start(self):
        ai = self._mode.get() == 'ai'
        self.result = {
            'ai_enabled':    ai,
            'ai_strategy':   self._strategy.get(),
            'ai_depth':      self._depth.get(),
            'ai_time_limit': self._time.get(),
        }
        self.root.destroy()

    def _on_close(self):
        self.result = None
        self.root.destroy()


# ─────────────────────────────────────────────────────────────────────────────
#  GAME GUI
# ─────────────────────────────────────────────────────────────────────────────
class CheckerGUI:

    def __init__(self, ai_enabled=False, ai_strategy='AlphaBetaOrdering',
                 ai_depth=7, ai_time_limit=3.0):

        mode = 'Human vs AI' if ai_enabled else 'Human vs Human'
        self.root = tk.Tk()
        self.root.title(f'Checkers  —  {mode}')
        self.root.configure(bg=T['bg'])
        self.root.resizable(False, False)

        self.sq       = 64
        self.margin   = 24
        self.board_px = BOARD_SIZE * self.sq          # 512
        self.canvas_w = self.board_px + 2 * self.margin  # 560
        self.canvas_h = self.canvas_w                 # 560

        self.game_board            = GameBoard()
        self.current_player        = WHITE
        self.selected_pos          = None
        self.valid_moves           = []
        self.game_over             = False
        self.must_continue_jumping = False
        self.move_counter          = 0
        self.wants_new_game        = False
        self.go_back_to_menu       = False

        self.ai_enabled      = ai_enabled
        self.ai_player       = BLACK
        self.ai_depth        = ai_depth
        self.ai_time_limit   = ai_time_limit
        self.ai_move_logs    = []
        self.game_start_time = time.time()

        if ai_enabled:
            strategies = {
                'Minimax':           MinimaxSearch,
                'AlphaBeta':         AlphaBetaSearch,
                'AlphaBetaOrdering': AlphaBetaWithOrdering,
            }
            cls = strategies.get(ai_strategy, AlphaBetaWithOrdering)
            self.ai_search        = cls(ai_depth, ai_time_limit)
            self.ai_strategy_name = ai_strategy

        _center_window(self.root, WIN_W, WIN_H)
        self._build_ui()
        self.root.protocol('WM_DELETE_WINDOW', self._on_close)
        self.draw_board()
        self.root.mainloop()

    # ── layout ────────────────────────────────────────────────────────────────
    def _build_ui(self):
        outer = tk.Frame(self.root, bg=T['bg'])
        outer.pack(fill=tk.BOTH, expand=True, padx=14, pady=14)

        left = tk.Frame(outer, bg=T['bg'])
        left.pack(side=tk.LEFT, fill=tk.BOTH)
        self._build_header(left)
        self._build_board(left)
        self._build_status_bar(left)

        right = tk.Frame(outer, bg=T['bg'], width=330)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(14, 0))
        right.pack_propagate(False)
        # Buttons anchored to bottom first, then history fills remaining space
        self._build_buttons(right)
        if self.ai_enabled:
            self._build_analytics_panel(right)
        self._build_history_panel(right)

    def _build_header(self, parent):
        bar = tk.Canvas(parent, height=54, bg=T['bg'], highlightthickness=0,
                        width=self.canvas_w)
        bar.pack(pady=(0, 10))
        _rounded(bar, 0, 0, self.canvas_w, 52, r=10,
                 fill=T['card'], outline=T['border'], width=1)
        bar.create_text(18, 26, anchor='w', text='CHECKERS',
                        font=FONT_TITLE, fill=T['white'])
        self._turn_canvas  = bar
        self._turn_text_id = bar.create_text(
            self.canvas_w - 18, 26, anchor='e', text="WHITE'S TURN",
            font=FONT_HEADER, fill=T['text'])

    def _set_turn_text(self, txt, color=None):
        self._turn_canvas.itemconfig(
            self._turn_text_id, text=txt, fill=color or T['text'])

    def _build_board(self, parent):
        frame = tk.Frame(parent, bg=T['bg'])
        frame.pack()
        self.canvas = tk.Canvas(frame,
                                width=self.canvas_w, height=self.canvas_h,
                                bg=T['bg'], highlightthickness=0)
        self.canvas.pack()
        self.canvas.bind('<Button-1>', self.on_canvas_click)

    def _build_status_bar(self, parent):
        self.status_var = tk.StringVar(value='Select a piece to move')
        bar = tk.Canvas(parent, height=38, bg=T['bg'], highlightthickness=0,
                        width=self.canvas_w)
        bar.pack(pady=(10, 0))
        _rounded(bar, 0, 0, self.canvas_w, 36, r=8,
                 fill=T['card'], outline=T['border'], width=1)
        self._status_text_id = bar.create_text(
            self.canvas_w // 2, 18, text=self.status_var.get(),
            font=FONT_BODY, fill=T['text_dim'])

        def _sync(*_):
            bar.itemconfig(self._status_text_id, text=self.status_var.get())
        self.status_var.trace_add('write', _sync)

    # ── analytics panel ───────────────────────────────────────────────────────
    def _build_analytics_panel(self, parent):
        outer = tk.Canvas(parent, bg=T['bg'], highlightthickness=0, height=226)
        outer.pack(fill=tk.X, pady=(0, 10))

        def _draw(_e=None):
            outer.delete('all')
            w = outer.winfo_width() or 320
            _rounded(outer, 0, 0, w, 224, r=10,
                     fill=T['card'], outline=T['border'])
            outer.create_text(16, 20, anchor='w', text='AI  ANALYTICS',
                              font=FONT_HEADER, fill=T['text'])
            y = 46
            for lbl, val in [('Strategy',  self.ai_strategy_name),
                              ('Max depth', str(self.ai_depth)),
                              ('Time limit', f'{self.ai_time_limit}s')]:
                outer.create_text(20, y, anchor='w', text=lbl,
                                  font=FONT_SMALL, fill=T['text_lo'])
                outer.create_text(w - 20, y, anchor='e', text=val,
                                  font=('Segoe UI', 9, 'bold'), fill=T['text_dim'])
                y += 20
            outer.create_line(16, y + 4, w - 16, y + 4,
                              fill=T['border'], width=1)
            y += 18
            outer.create_text(16, y, anchor='w', text='Last Move Stats',
                              font=('Segoe UI', 10, 'bold'), fill=T['accent'])
            y += 24
            self.analytics_labels = {}
            rows = [
                ('Nodes expanded', 'nodes',  T['val_a']),
                ('Nodes pruned',   'prunes', T['val_b']),
                ('Depth reached',  'depth',  T['val_a']),
                ('Time elapsed',   'time',   T['val_b']),
            ]
            for lbl, key, col in rows:
                outer.create_text(20, y, anchor='w', text=lbl,
                                  font=FONT_SMALL, fill=T['text_lo'])
                tid = outer.create_text(w - 20, y, anchor='e', text='—',
                                        font=('Segoe UI', 9, 'bold'), fill=col)
                self.analytics_labels[key] = tid
                y += 22

        self._analytics_canvas = outer
        outer.bind('<Configure>', _draw)
        _draw()

    # ── history panel ─────────────────────────────────────────────────────────
    def _build_history_panel(self, parent):
        wrapper = tk.Frame(parent, bg=T['card'], bd=0)
        wrapper.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        hdr = tk.Canvas(wrapper, height=34, bg=T['card'], highlightthickness=0)
        hdr.pack(fill=tk.X)
        hdr.create_text(14, 17, anchor='w', text='MOVE  HISTORY',
                        font=FONT_HEADER, fill=T['text'])

        tk.Frame(wrapper, bg=T['border'], height=1).pack(fill=tk.X)

        self.history_text = scrolledtext.ScrolledText(
            wrapper, font=FONT_MONO,
            bg=T['bg'], fg=T['text'],
            insertbackground=T['text'],
            selectbackground=T['btn_bg'],
            relief=tk.FLAT, padx=10, pady=8,
            wrap=tk.WORD, state='disabled', bd=0)
        self.history_text.pack(fill=tk.BOTH, expand=True, padx=4, pady=(0, 4))

        self.history_text.tag_config('white_mv',
                                     foreground=T['pw'],
                                     font=(FONT_MONO[0], 9, 'bold'))
        self.history_text.tag_config('black_mv',
                                     foreground=T['text_dim'],
                                     font=(FONT_MONO[0], 9, 'bold'))
        self.history_text.tag_config('capture',
                                     foreground=T['val_a'],
                                     font=(FONT_MONO[0], 9, 'bold'))
        self.history_text.tag_config('king',
                                     foreground=T['white'],
                                     font=(FONT_MONO[0], 9, 'bold'))
        self.history_text.tag_config('info',
                                     foreground=T['text_lo'],
                                     font=(FONT_MONO[0], 9, 'italic'))
        self._write_history_header()

    def _write_history_header(self):
        h = self.history_text
        h.config(state='normal')
        h.delete('1.0', tk.END)
        h.insert(tk.END, '  Game started\n', 'info')
        h.insert(tk.END, '  ' + '─' * 22 + '\n', 'info')
        h.config(state='disabled')

    # ── buttons ───────────────────────────────────────────────────────────────
    def _build_buttons(self, parent):
        row = tk.Frame(parent, bg=T['bg'])
        row.pack(side=tk.BOTTOM, fill=tk.X, pady=(6, 0))

        for text, cmd, expand, pad in [
            ('NEW  GAME', self.new_game,   True,  (0, 6)),
            ('MENU',      self.go_to_menu, False, (0, 0)),
        ]:
            btn = tk.Button(row, text=text, font=FONT_HEADER,
                            fg=T['text'], bg=T['btn_bg'],
                            activebackground=T['btn_h'],
                            activeforeground=T['white'],
                            relief=tk.FLAT, bd=0,
                            padx=18, pady=10,
                            cursor='hand2', command=cmd)
            btn.pack(side=tk.LEFT, fill=tk.X, expand=expand, padx=pad)
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg=T['btn_h']))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg=T['btn_bg']))

    # ── board drawing ─────────────────────────────────────────────────────────
    def draw_board(self):
        c = self.canvas
        c.delete('all')
        m, sq, bpx = self.margin, self.sq, self.board_px

        # outer frame
        c.create_rectangle(m - 4, m - 4, m + bpx + 4, m + bpx + 4,
                           fill=T['sq_frame'], outline=T['sq_frame'])

        # squares
        for r in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x1 = m + col * sq
                y1 = m + r   * sq
                color = T['sq_dark'] if (r + col) % 2 else T['sq_light']
                c.create_rectangle(x1, y1, x1 + sq, y1 + sq,
                                   fill=color, outline=T['sq_frame'], width=1)

        # coordinates
        for i in range(BOARD_SIZE):
            c.create_text(m // 2, m + i * sq + sq // 2,
                          text=str(i + 1), font=FONT_SMALL, fill=T['coord'])
            c.create_text(m + i * sq + sq // 2, m + bpx + m // 2,
                          text=chr(ord('a') + i), font=FONT_SMALL, fill=T['coord'])

        # selection & move indicators
        if self.selected_pos:
            sr, sc = self.selected_pos
            x1 = m + sc * sq
            y1 = m + sr * sq
            c.create_rectangle(x1 + 2, y1 + 2, x1 + sq - 2, y1 + sq - 2,
                               outline=T['sel'], width=2)
            fr, fc = self.selected_pos
            for tr, tc in self.valid_moves:
                xc = m + tc * sq + sq // 2
                yc = m + tr * sq + sq // 2
                if abs(tr - fr) == 2:
                    c.create_oval(xc - 18, yc - 18, xc + 18, yc + 18,
                                  fill=T['jump_fill'], outline=T['jump_ring'], width=2)
                    c.create_text(xc, yc, text='×',
                                  font=('Segoe UI', 14, 'bold'), fill=T['accent'])
                else:
                    c.create_oval(xc - 11, yc - 11, xc + 11, yc + 11,
                                  fill=T['move_fill'], outline=T['move_ring'], width=2)

        self._draw_pieces()

    def _draw_pieces(self):
        c = self.canvas
        m, sq = self.margin, self.sq
        for r in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.game_board.board[r][col]
                if piece == EMPTY:
                    continue
                xc  = m + col * sq + sq // 2
                yc  = m + r   * sq + sq // 2
                rad = sq // 2 - 6

                # drop shadow
                c.create_oval(xc - rad + 3, yc - rad + 3,
                              xc + rad + 3, yc + rad + 3,
                              fill=T['shadow'], outline='')

                if piece in (WHITE, WHITE_KING):
                    fill, inner, ring = T['pw'], T['pw_in'], T['ring_w']
                else:
                    fill, inner, ring = T['pb'], T['pb_in'], T['ring_b']

                c.create_oval(xc - rad,     yc - rad,
                              xc + rad,     yc + rad,
                              fill=fill, outline=ring, width=3)
                c.create_oval(xc - rad + 8, yc - rad + 8,
                              xc + rad - 8, yc + rad - 8,
                              fill=inner, outline='')

                if piece == WHITE_KING:
                    c.create_text(xc, yc + 1, text='K',
                                  font=('Segoe UI', 12, 'bold'), fill=T['ring_b'])
                elif piece == BLACK_KING:
                    c.create_text(xc, yc + 1, text='K',
                                  font=('Segoe UI', 12, 'bold'), fill=T['ring_w'])

    # ── move logic ────────────────────────────────────────────────────────────
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
        tag    = 'white_mv' if player == WHITE else 'black_mv'
        icon   = '○' if player == WHITE else '●'
        ai_tag = ' AI' if is_ai else ''
        h.insert(tk.END, f' {self.move_counter:>3}. {icon}{ai_tag} ', tag)
        h.insert(tk.END,
                 f'({start[0]+1},{start[1]+1}) → ({end[0]+1},{end[1]+1})')
        if was_jump:
            h.insert(tk.END, '  ×capture', 'capture')
        if promoted:
            h.insert(tk.END, '  ♛king!', 'king')
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
                      for c in row if c.upper() == WHITE)
        black_n = sum(1 for row in self.game_board.board
                      for c in row if c.upper() == BLACK)
        winner = None
        if white_n == 0:
            winner = 'BLACK'
        elif black_n == 0:
            winner = 'WHITE'
        elif not self.game_board.has_any_legal_move(self.current_player):
            winner = 'BLACK' if self.current_player == WHITE else 'WHITE'
        if winner:
            self.game_over = True
            self.status_var.set(f'{winner}  WINS!')
            self._set_turn_text(f'GAME OVER  —  {winner} WINS!', T['white'])
            h = self.history_text
            h.config(state='normal')
            h.insert(tk.END, '\n  ' + '─' * 22 + '\n', 'info')
            h.insert(tk.END, f'  {winner} WINS!\n',
                     'white_mv' if winner == 'WHITE' else 'black_mv')
            h.config(state='disabled')
            h.see(tk.END)
            self._save_log(winner)
            return True
        return False

    def on_canvas_click(self, event):
        if self.game_over:
            return
        m   = self.margin
        col = (event.x - m) // self.sq
        row = (event.y - m) // self.sq
        if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
            return
        piece = self.game_board.board[row][col]

        if self.must_continue_jumping and self.selected_pos:
            fr, fc = self.selected_pos
            if (row, col) in self.valid_moves:
                result = self.game_board.make_move(fr, fc, row, col, self.current_player)
                self.add_move_to_history(self.current_player, (fr, fc), (row, col),
                                         result['was_jump'], result['promoted'], False)
                jumps = [(r, c) for r, c in self.get_valid_moves(row, col)
                         if abs(r - row) == 2]
                if jumps:
                    self.selected_pos, self.valid_moves = (row, col), jumps
                    self.must_continue_jumping = True
                    self.status_var.set(f'Continue jumping!  ({len(jumps)} available)')
                else:
                    self.status_var.set('Multi-jump complete')
                    self.selected_pos, self.valid_moves = None, []
                    self.must_continue_jumping = False
                    if not self.check_game_over():
                        self.switch_turn()
                self.draw_board()
            return

        if piece in [self.current_player, self.current_player.lower()]:
            self.selected_pos = (row, col)
            self.valid_moves  = self.get_valid_moves(row, col)
            j = sum(1 for r2, c2 in self.valid_moves if abs(r2 - row) == 2)
            n = len(self.valid_moves) - j
            self.status_var.set(f'{j} capture(s)   {n} move(s)')
            self.draw_board()
            return

        if self.selected_pos:
            fr, fc = self.selected_pos
            if (row, col) in self.valid_moves:
                result  = self.game_board.make_move(fr, fc, row, col, self.current_player)
                is_jump = abs(row - fr) == 2
                self.add_move_to_history(self.current_player, (fr, fc), (row, col),
                                         result['was_jump'], result['promoted'], False)
                if is_jump:
                    jumps = [(r2, c2) for r2, c2 in self.get_valid_moves(row, col)
                             if abs(r2 - row) == 2]
                    if jumps:
                        self.selected_pos, self.valid_moves = (row, col), jumps
                        self.must_continue_jumping = True
                        self.status_var.set(f'Must continue jump!  ({len(jumps)} available)')
                        self.draw_board()
                        return
                self.status_var.set('Move complete')
                self.selected_pos, self.valid_moves = None, []
                self.must_continue_jumping = False
                if not self.check_game_over():
                    self.switch_turn()
                self.draw_board()
            else:
                self.status_var.set('Invalid — click a highlighted square')

    def switch_turn(self):
        self.current_player = BLACK if self.current_player == WHITE else WHITE
        if self.ai_enabled and self.current_player == self.ai_player:
            self._set_turn_text('AI  THINKING ...', T['accent'])
            self.status_var.set(f'AI thinking  ({self.ai_strategy_name}) ...')
            self.root.after(100, self.make_ai_move)
        else:
            who = 'WHITE' if self.current_player == WHITE else 'BLACK'
            self._set_turn_text(f"{who}'S TURN")
            self.status_var.set('Select a piece to move')

    def make_ai_move(self):
        if self.game_over:
            return
        self.root.update()
        best_move = self.ai_search.GetBestMove(self.game_board, self.current_player)
        if best_move is None:
            self.status_var.set('AI has no legal moves')
            self.check_game_over()
            return
        sr, sc = best_move.StartingMoveLocation
        tr, tc = best_move.DestinationLocation
        result  = self.game_board.make_move(sr, sc, tr, tc, self.current_player)
        self.add_move_to_history(self.current_player, (sr, sc), (tr, tc),
                                 result['was_jump'], result['promoted'], True)
        if hasattr(self.ai_search, 'Analytics'):
            self.update_analytics_display(self.ai_search.Analytics)
            a = self.ai_search.Analytics
            self.ai_move_logs.append({
                'move_num':  self.move_counter,
                'move_text': f'BLACK AI  ({sr+1},{sc+1})->({tr+1},{tc+1})',
                'nodes':     a.NumberNodesExpanded,
                'prunes':    a.NumberNodesPruned,
                'depth':     a.MaxDepthReached,
                'time':      a.GetTimeElapsed() if hasattr(a, 'GetTimeElapsed') else 0.0,
            })
        desc = f'AI  ({sr+1},{sc+1}) → ({tr+1},{tc+1})'
        if result['was_jump']:
            desc += '  capture'
        if result['promoted']:
            desc += '  KING!'
        self.status_var.set(desc)
        self.draw_board()
        if not self.check_game_over():
            self.switch_turn()

    # ── game lifecycle ────────────────────────────────────────────────────────
    def new_game(self):
        if self.move_counter > 0:
            self._save_log(None)
        self.wants_new_game  = True
        self.go_back_to_menu = False
        self.root.destroy()

    def go_to_menu(self):
        if self.move_counter > 0:
            self._save_log(None)
        self.wants_new_game  = True
        self.go_back_to_menu = True
        self.root.destroy()

    def _save_log(self, winner=None):
        from OtherStuff import save_game_log
        ai_config = None
        if self.ai_enabled:
            ai_config = {
                'strategy':   self.ai_strategy_name,
                'depth':      self.ai_depth,
                'time_limit': self.ai_time_limit,
            }
        history = [ln.strip()
                   for ln in self.history_text.get('1.0', tk.END).strip().splitlines()
                   if ln.strip()]
        path = save_game_log({
            'mode':         'Human vs AI' if self.ai_enabled else 'Human vs Human',
            'interface':    'GUI',
            'winner':       winner,
            'total_moves':  self.move_counter,
            'move_history': history,
            'ai_config':    ai_config,
            'ai_move_logs': self.ai_move_logs,
        })
        print(f'Analytics log saved -> {path}')

    def _on_close(self):
        if self.move_counter > 0:
            winner = None
            if self.game_over:
                wb = sum(1 for row in self.game_board.board
                         for c in row if c.upper() == WHITE)
                bb = sum(1 for row in self.game_board.board
                         for c in row if c.upper() == BLACK)
                winner = 'WHITE' if bb == 0 else ('BLACK' if wb == 0 else None)
            self._save_log(winner)
        self.root.destroy()


# ─────────────────────────────────────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────
def launch():
    cfg_result = None
    while True:
        if cfg_result is None:
            cfg = ConfigScreen()
            if cfg.result is None:
                break
            cfg_result = cfg.result
        game = CheckerGUI(**cfg_result)
        if not game.wants_new_game:
            break
        if game.go_back_to_menu:
            cfg_result = None


if __name__ == '__main__':
    launch()
