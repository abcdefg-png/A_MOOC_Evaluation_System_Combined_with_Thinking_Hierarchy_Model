import matplotlib.pyplot as plt
import matplotlib
import output
import input
import pandas as pd
import os

if __name__ == "__main__":
    matplotlib.rcParams['pdf.fonttype'] = 42
    matplotlib.rcParams['ps.fonttype'] = 42

    if not os.path.exists("output"):
        os.makedirs("output")
    data = input.input()
    out = []
    for questionnaire in data:
        for question in questionnaire:
            out.append(
                output.print_csv(question['filename'], question['id'], question['allans'], question['guessmatrix'],
                                 ansnum=question['ansnum']))
            output.print_heatmap(question['filename'], question['id'], question['allans'], question['guessmatrix'],
                                 order=range(len(question['allans']) - 1, -1, -1),
                                 specialname=question['specialname'] if 'specialname' in question else None,
                                 ansnum=question['ansnum'], method="original")
            output.print_heatmap(question['filename'], question['id'], question['allans'], question['guessmatrix'],
                                 specialname=question['specialname'] if 'specialname' in question else None,
                                 ansnum=question['ansnum'], method="default")
            output.print_heatmap(question['filename'], question['id'], question['allans'], question['guessmatrix'],
                                 specialname=question['specialname'] if 'specialname' in question else None,
                                 ansnum=question['ansnum'], method="variant")
    names = ["filename", "id", "allans", "optimal partition", "optimal order corresponding to the optimal partition",
             "frobinius norm of optimal partition", "optimal order of default algorithm",
             "frobinius norm of default algorithm"]
    data = pd.DataFrame(columns=names, data=out)
    data.to_csv("output.csv")
