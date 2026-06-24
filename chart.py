import argparse
import csv
import sys
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


# ── palette ──────────────────────────────────────────────────────────────────

BG_FIGURE = '#0d1117'
BG_AXES   = '#161b22'
C_EDGE    = '#30363d'
C_GRID    = '#21262d'
C_TEXT    = '#e6edf3'
C_MUTE    = '#8b949e'
C_ASYNC   = '#3dd9a4'   # teal
C_SEQ     = '#f87171'   # coral
C_THREAD  = '#fbbf24'   # amber


# ── theme ─────────────────────────────────────────────────────────────────────

def apply_theme():
    plt.rcParams.update({
        'figure.facecolor': BG_FIGURE,
        'axes.facecolor':   BG_AXES,
        'axes.edgecolor':   C_EDGE,
        'axes.labelcolor':  C_TEXT,
        'text.color':       C_TEXT,
        'xtick.color':      C_MUTE,
        'ytick.color':      C_MUTE,
        'xtick.labelsize':  10,
        'ytick.labelsize':  10,
        'axes.titlesize':   14,
        'axes.titlepad':    14,
        'axes.labelsize':   12,
        'axes.labelpad':    8,
        'grid.color':       C_GRID,
        'grid.linewidth':   0.8,
        'legend.facecolor': '#1c2128',
        'legend.edgecolor': C_EDGE,
        'legend.fontsize':  11,
        'font.family':      'sans-serif',
    })


def style_ax(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(C_EDGE)
    ax.spines['bottom'].set_color(C_EDGE)
    ax.grid(True, which='major', alpha=0.5)
    ax.grid(True, which='minor', alpha=0.15)


# ── data ──────────────────────────────────────────────────────────────────────

def read_csv(path):
    path = Path(path)
    if not path.exists():
        sys.exit(f'Error: file not found — {path}')
    packets, times = [], []
    with open(path, newline='') as f:
        for row in csv.DictReader(f):
            packets.append(int(row['Total_Packets']))
            times.append(float(row['Total_Time']))
    return packets, times


# ── axis formatters ───────────────────────────────────────────────────────────

def fmt_x(v, _):
    v = int(v)
    return f'{v // 1000}k' if v >= 1000 else str(v)

def fmt_y_sec(v, _):
    return f'{v / 1000:.1f}k' if v >= 1000 else f'{v:.0f}'


# ── charts ────────────────────────────────────────────────────────────────────

def chart_time(a_p, a_t, s_p, s_t, t_p, t_t):
    """Chart 1 — raw time vs packet count, all three approaches."""
    fig, ax = plt.subplots(figsize=(11, 6.5))

    ax.plot(a_p, a_t, color=C_ASYNC,  marker='o', lw=2.2, ms=5.5, label='Async')
    ax.plot(s_p, s_t, color=C_SEQ,    marker='s', lw=2.2, ms=5.5, label='Sequential', ls='--')
    ax.plot(t_p, t_t, color=C_THREAD, marker='^', lw=2.2, ms=5.5, label='Threading',  ls=':')

    ax.set_xscale('log')
    ax.set_xlabel('total packets')
    ax.set_ylabel('time (seconds)')
    ax.set_title('time vs packets')
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(fmt_x))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(fmt_y_sec))
    style_ax(ax)
    ax.legend()
    fig.tight_layout()
    return fig


def chart_speedup(a_p, a_t, s_p, s_t, t_p, t_t):
    """Chart 2 — how many times slower sequential and threading are vs async."""
    a_map = dict(zip(a_p, a_t))
    s_map = dict(zip(s_p, s_t))
    t_map = dict(zip(t_p, t_t))
    pts = sorted(set(a_p) & set(s_p) & set(t_p))

    s_ratio = [s_map[p] / a_map[p] for p in pts]
    t_ratio = [t_map[p] / a_map[p] for p in pts]

    fig, ax = plt.subplots(figsize=(11, 6.5))

    ax.plot(pts, s_ratio, color=C_SEQ,    marker='s', lw=2.2, ms=5.5, label='Sequential / async', ls='--')
    ax.plot(pts, t_ratio, color=C_THREAD, marker='^', lw=2.2, ms=5.5, label='Threading / async',  ls=':')
    ax.axhline(1, color=C_ASYNC, lw=1.5, alpha=0.55, label='Async baseline (1×)')

    peak_i = s_ratio.index(max(s_ratio))
    ax.annotate(
        f'{s_ratio[peak_i]:.1f}×',
        xy=(pts[peak_i], s_ratio[peak_i]),
        xytext=(8, 6), textcoords='offset points',
        color=C_SEQ, fontsize=10,
    )

    ax.set_xscale('log')
    ax.set_xlabel('total packets')
    ax.set_ylabel('times slower than async')
    ax.set_title('speedup — sequential and threading relative to async')
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(fmt_x))
    style_ax(ax)
    ax.legend()
    fig.tight_layout()
    return fig


def chart_per_packet(a_p, a_t, s_p, s_t, t_p, t_t):
    """Chart 3 — time per packet; shows concurrency efficiency clearly."""
    fig, ax = plt.subplots(figsize=(11, 6.5))

    ax.plot(a_p, [t / p for p, t in zip(a_p, a_t)], color=C_ASYNC,  marker='o', lw=2.2, ms=5.5, label='Async')
    ax.plot(s_p, [t / p for p, t in zip(s_p, s_t)], color=C_SEQ,    marker='s', lw=2.2, ms=5.5, label='Sequential', ls='--')
    ax.plot(t_p, [t / p for p, t in zip(t_p, t_t)], color=C_THREAD, marker='^', lw=2.2, ms=5.5, label='Threading',  ls=':')

    ax.set_xscale('log')
    ax.set_xlabel('total packets')
    ax.set_ylabel('seconds per packet')
    ax.set_title('time per packet')
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(fmt_x))
    style_ax(ax)
    ax.legend()
    fig.tight_layout()
    return fig


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    ASYNC_PATH  = 'async/results/async_results.csv'
    SEQ_PATH    = 'sequential/results/sequential_results.csv'
    THREAD_PATH = 'threading/results/threading_results.csv'
    OUTPUT_DIR  = '.'
    DPI         = 150

    out = Path(OUTPUT_DIR)
    out.mkdir(parents=True, exist_ok=True)

    print('Reading data...')
    a_p, a_t = read_csv(ASYNC_PATH)
    s_p, s_t = read_csv(SEQ_PATH)
    t_p, t_t = read_csv(THREAD_PATH)

    apply_theme()

    charts = [
        ('chart1_time_vs_packets.png', chart_time),
        ('chart2_speedup_ratio.png',   chart_speedup),
        ('chart3_time_per_packet.png', chart_per_packet),
    ]

    save_kw = dict(dpi=DPI, bbox_inches='tight', facecolor=BG_FIGURE)

    for name, fn in charts:
        print(f'  → {name}')
        fig = fn(a_p, a_t, s_p, s_t, t_p, t_t)
        fig.savefig(out / name, **save_kw)
        plt.close(fig)

    print(f'\nDone — charts saved to: {out.resolve()}')


if __name__ == '__main__':
    main()