import tkinter as tk
from tkinter import font

# --- Configuration for Scoring and Fonts ---
# Based on the provided example, the penalty seems to be -3 per gap.
# A match is typically +1 or +5, and a mismatch 0 or -1. 
# We'll use standard: Match +5, Mismatch -1, Gap -3.
GAP_PENALTY = -3
MATCH_SCORE = 5
MISMATCH_SCORE = -1

FONT_FAMILY = "Courier New" # Fixed-width font for matrix
FONT_SIZE = 12

def calculate_needleman_wunsch():
    # 1. Get input sequences
    seq1 = entry_seq1.get().upper()
    seq2 = entry_seq2.get().upper()

    if not seq1 or not seq2:
        output_text.set("Please enter two DNA strands.")
        return

    m = len(seq1)
    n = len(seq2)

    # 2. Initialize the dynamic programming matrix S with (row, column) = (m+1, n+1)
    score_matrix = [[0 for _ in range(n + 1)] for _ in range(m + 1)]

    # 3. Apply the initializations from the formula: S[0,0] = 0
    # And initialize top row and left column with gap penalties
    for i in range(1, m + 1):
        score_matrix[i][0] = i * GAP_PENALTY
    for j in range(1, n + 1):
        score_matrix[0][j] = j * GAP_PENALTY

    # 4. Fill the matrix using the recursive formula from image 0
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # Calculate substitution score w(a_i, b_j)
            sub_score = MATCH_SCORE if seq1[i-1] == seq2[j-1] else MISMATCH_SCORE
            
            # Application of the formula:
            # S[i,j] = max of {
            #    gap from top (deletion): S[i-1,j] + w(a_i,-) -> GAP_PENALTY
            #    gap from left (insertion): S[i,j-1] + w(-,b_j) -> GAP_PENALTY
            #    diagonal (match/mismatch): S[i-1,j-1] + w(a_i,b_j)
            # }
            score_matrix[i][j] = max(
                score_matrix[i - 1][j] + GAP_PENALTY,
                score_matrix[i][j - 1] + GAP_PENALTY,
                score_matrix[i - 1][j - 1] + sub_score
            )

    # 5. Form formatted matrix for GUI display
    display_matrix_text(score_matrix, seq1, seq2)

    # 6. Trace back to find the optimal alignment
    align1 = ""
    align2 = ""
    i, j = m, n
    while i > 0 and j > 0:
        score_current = score_matrix[i][j]
        score_diagonal = score_matrix[i-1][j-1]
        score_up = score_matrix[i-1][j]
        score_left = score_matrix[i][j-1]

        sub_score = MATCH_SCORE if seq1[i-1] == seq2[j-1] else MISMATCH_SCORE

        if score_current == score_diagonal + sub_score:
            align1 = seq1[i-1] + align1
            align2 = seq2[j-1] + align2
            i -= 1
            j -= 1
        elif score_current == score_up + GAP_PENALTY:
            align1 = seq1[i-1] + align1
            align2 = "-" + align2
            i -= 1
        else: # gap in sequence 1
            align1 = "-" + align1
            align2 = seq2[j-1] + align2
            j -= 1

    # Finish trace back for remaining gaps at top/left
    while i > 0:
        align1 = seq1[i-1] + align1
        align2 = "-" + align2
        i -= 1
    while j > 0:
        align1 = "-" + align1
        align2 = seq2[j-1] + align2
        j -= 1

    # Update output
    output_str = f"Best score: {score_matrix[m][n]}\n\n"
    output_str += "Optimal Alignment:\n"
    output_str += f"{align1}\n{align2}"
    output_text.set(output_str)


def display_matrix_text(matrix, seq1, seq2):
    """Formats the DP matrix into a clean text grid for display."""
    m = len(matrix)
    n = len(matrix[0])
    
    matrix_text.config(state=tk.NORMAL)
    matrix_text.delete('1.0', tk.END)

    # Calculate max column width for alignment
    max_val = max(max(row) for row in matrix)
    min_val = min(min(row) for row in matrix)
    max_len = max(len(str(max_val)), len(str(min_val)), 1) + 1
    col_fmt = f"{{:>{max_len}}}" # Fixed-width formatting

    header = " " * (max_len + 1)
    for char in " " + seq2:
        header += col_fmt.format(char)
    matrix_text.insert(tk.END, header + "\n")

    for i, row in enumerate(matrix):
        row_char = " " if i == 0 else seq1[i-1]
        line = f"{row_char:>{max_len}} "
        for val in row:
            line += col_fmt.format(val)
        matrix_text.insert(tk.END, line + "\n")
    
    matrix_text.config(state=tk.DISABLED)


# --- GUI Setup ---
root = tk.Tk()
root.title("Needleman-Wunsch DNA Aligner")

# Use a fixed-width font for the entire GUI to maintain grid alignment
app_font = font.Font(family=FONT_FAMILY, size=FONT_SIZE)
root.option_add("*Font", app_font)

frame_inputs = tk.Frame(root)
frame_inputs.pack(pady=10)

tk.Label(frame_inputs, text="DNA Strand 1 (Vertical):").grid(row=0, column=0, sticky="e", padx=5)
entry_seq1 = tk.Entry(frame_inputs)
entry_seq1.grid(row=0, column=1)

tk.Label(frame_inputs, text="DNA Strand 2 (Horizontal):").grid(row=1, column=0, sticky="e", padx=5)
entry_seq2 = tk.Entry(frame_inputs)
entry_seq2.grid(row=1, column=1)

btn_align = tk.Button(root, text="Calculate Best Alignment", command=calculate_needleman_wunsch)
btn_align.pack(pady=10)

frame_results = tk.Frame(root)
frame_results.pack(pady=10, fill=tk.BOTH, expand=True)

tk.Label(frame_results, text="Calculation Matrix:").pack()
matrix_text = tk.Text(frame_results, state=tk.DISABLED, wrap=tk.NONE, width=60, height=20)
matrix_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Add scrollbars for matrix
yscroll = tk.Scrollbar(frame_results, command=matrix_text.yview)
yscroll.pack(side=tk.RIGHT, fill=tk.Y)
matrix_text.config(yscrollcommand=yscroll.set)

xscroll = tk.Scrollbar(root, orient=tk.HORIZONTAL, command=matrix_text.xview)
xscroll.pack(fill=tk.X)
matrix_text.config(xscrollcommand=xscroll.set)

tk.Label(root, text="Alignment:").pack(pady=(10, 0))
output_text = tk.StringVar()
output_label = tk.Label(root, textvariable=output_text, justify=tk.LEFT, background="#f0f0f0", relief=tk.SUNKEN, padx=10, pady=5)
output_label.pack(fill=tk.X, padx=10, pady=(0, 10))

root.mainloop()