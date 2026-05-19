import yaml
import pandas as pd
import argparse
import os

# (latex_header, yaml_key, multiplier, format_string)
# Use \\% so the output file contains \% — the correct LaTeX escaped percent sign.
COLUMNS = [
    ('EER (\\%)',  'eer',       100, '{:.2f}'),
    ('AUC',        'auc',       1,   '{:.4f}'),
    ('Acc (\\%)',  'accuracy',  100, '{:.2f}'),
    ('TPR (\\%)',  'tpr',       100, '{:.2f}'),
    ('TNR (\\%)',  'tnr',       100, '{:.2f}'),
    ('Pre (\\%)',  'precision', 100, '{:.2f}'),
    ('F1',         'f1',        1,   '{:.4f}'),
    ('TP',         'tp',        1,   '{:.0f}'),
    ('TN',         'tn',        1,   '{:.0f}'),
    ('FP',         'fp',        1,   '{:.0f}'),
    ('FN',         'fn',        1,   '{:.0f}'),
]

NA = 'N/A'


def _format_row(metrics):
    is_single_class = metrics.get('eer', -1) == -1
    row = {}
    for header, key, mult, fmt in COLUMNS:
        val = metrics.get(key)
        if is_single_class or val is None or val == -1:
            row[header] = NA
        else:
            row[header] = fmt.format(val * mult)
    return row


def generate_latex_from_metrics(metric_file_path, output_path=None):
    """
    Reads a YAML metrics file and generates a LaTeX table.

    Args:
        metric_file_path (str): Path to the metrics YAML file produced by evaluate.py.
        output_path (str, optional): If given, writes the .tex file here; otherwise prints.
    """
    if not os.path.exists(metric_file_path):
        raise FileNotFoundError(f"Metric file not found at: {metric_file_path}")

    with open(metric_file_path, 'r') as f:
        metrics_data = yaml.safe_load(f)

    if not metrics_data:
        print("No data to generate table.")
        return

    # Individual datasets first (in evaluation order), Average pinned to the bottom.
    table_data = {}
    for name, metrics in metrics_data.items():
        if name != 'Average':
            table_data[name] = _format_row(metrics)

    if 'Average' in metrics_data:
        table_data['\\textbf{Average}'] = _format_row(metrics_data['Average'])

    df = pd.DataFrame.from_dict(table_data, orient='index')

    # l for the dataset name, r for every metric column
    col_fmt = 'l' + 'r' * len(COLUMNS)

    # pandas 2.x always emits booktabs rules (\toprule/\midrule/\bottomrule).
    # index_names=False suppresses the spurious blank index-name row in pandas 2.x.
    latex_str = df.to_latex(
        escape=False,           # preserves \textbf and \% literals
        column_format=col_fmt,
        na_rep=NA,
        index_names=False,
    )

    # Insert a \midrule separator above the Average row when it exists, then
    # collapse any double-midrule that arises when Average is the first data row.
    latex_str = latex_str.replace(
        '\\textbf{Average}',
        '\\midrule\n\\textbf{Average}',
    )
    latex_str = latex_str.replace('\\midrule\n\\midrule', '\\midrule')

    # Wrap in a full table environment ready to \input{} into a paper.
    # Use table* to span both columns in a two-column layout (suits wide tables).
    full_latex = (
        '% Required packages: \\usepackage{booktabs}\n'
        '\\begin{table*}[htbp]\n'
        '  \\centering\n'
        '  \\caption{Evaluation Results}\n'
        '  \\label{tab:results}\n'
        + latex_str +
        '\\end{table*}\n'
    )

    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(full_latex)
        print(f"\nLaTeX table saved to: {output_path}")
    else:
        print('-' * 80)
        print('LaTeX Table — paste into your .tex file:')
        print('-' * 80)
        print(full_latex)
        print('-' * 80)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Generate a LaTeX table from a metrics YAML file produced by evaluate.py."
    )
    parser.add_argument('metric_file', type=str, help="Path to the metrics YAML file.")
    parser.add_argument('--output_path', type=str, help="Optional path to save the .tex file.")
    args = parser.parse_args()

    generate_latex_from_metrics(args.metric_file, args.output_path)
