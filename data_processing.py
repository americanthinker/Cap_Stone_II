def punc_removal(bag_of_words):
    '''
    :param bag_of_words: str;
    :return: str with all punctuation removed
    Also removes 4, 3, and 2 blank spaces
    '''
    punc = "#$!%^&*()@-=_+]/[}{\|;':,./<>?`~\""
    for symbol in punc:
        bag_of_words = bag_of_words.replace(symbol, '').replace('    ', ' ')\
                       .replace('   ', ' ').replace('  ', ' ')
    return bag_of_words

def scaler(series, bottom_range, top_range):
    '''
    Scales data between a range between (bottom_range, top_range)
    𝑥𝑛𝑜𝑟𝑚𝑎𝑙𝑖𝑧𝑒𝑑=(𝑏−𝑎) * 𝑥−𝑚𝑖𝑛(𝑥)     + a
                    𝑚𝑎𝑥(𝑥)−𝑚𝑖𝑛(𝑥)
    Input: pd.Series, np.array (list will not broadcast)
    Ouput: scaled version of Input between bottom_range and top_range
    '''
    multiplier = top_range - bottom_range
    numerator = series - min(series)
    denominator = max(series) - min(series)
    ans = multiplier * numerator/denominator
    return ans + bottom_range


if __name__ == '__main__':

    import pandas as pd

    df = pd.read_csv('vets_coords.csv')
    nums = df['Combined']
    print(scaler(nums, 22, 4))