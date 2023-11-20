if __name__ == '__main__':
    import pandas as pd

    with open('result.txt', 'w') as f:
        f.write(str(float(pd.Series([1, 2, 4]).mean())))
