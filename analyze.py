import codecs
import re
import pandas
import numpy


def create_data_frame():
    with codecs.open('text.txt', encoding='utf-8') as f:
        years = []
        months = []
        days = []
        hours = []
        minutes = []
        names = []
        messages = []
        media = []
        lengths = []
        word_counts = []

        words = []
        word_names = []

        lines = f.readlines()
        full_text = ""
        for line in lines:
            full_text += line
        splits = re.split("(\d\d\.\d\d\.\d\d, \d\d:\d\d)", full_text)
        for i in range(1, len(splits), 2):
            time = splits[i]
            time_splits = re.split("(\d\d)", time)
            years.append(time_splits[5])
            months.append(time_splits[3])
            days.append(time_splits[1])

            hours.append(time_splits[7])
            minutes.append(time_splits[9])
            remains = splits[i+1]
            name_split = re.split("- ([^:]*)", remains)
            names.append(name_split[1])
            message = name_split[2].lstrip(": ")
            is_media = "<Medien ausgeschlossen>" in message
            if is_media:
                message = None
            media.append(is_media)

            messages.append(message)
            if message is not None:
                word_counts.append(len(message.split()))
                words.extend([word.lower() for word in message.split()])
                word_names.extend([name_split[1]]*len(message.split()))
                lengths.append(len(message))
            else:
                word_counts.append(None)
                lengths.append(None)

        df = pandas.DataFrame({"Year": years, "Month": months, "Day": days, "Hour": hours, "Minute": minutes,
                               "Names": names, "Messages": messages, "Media": media, "Word Count": word_counts,
                               "Length": lengths})

        df_words = pandas.DataFrame({"Names": word_names, "Words": words})

        return df, df_words


def out_put_analysis(df, df_words):
    with codecs.open("analysis.txt", "w", encoding="utf-8") as f:
        f.write("---MESSAGES---\n")
        f.write(f"Message Count: {df['Messages'].size}\n")
        f.write(f"Lukas Message Count: {df[df['Names'] == 'Lukas']['Messages'].size}\n")
        f.write(f"Lukas Message Count: {df[df['Names'] == 'Lukas']['Messages'].size/df['Messages'].size*100}%\n")
        f.write(f"Tobias Message Count: {df[df['Names'] == 'Tobias Jungbluth']['Messages'].size}\n")
        f.write(
            f"Tobias Message Count: {df[df['Names'] == 'Tobias Jungbluth']['Messages'].size/df['Messages'].size*100}%\n")

        f.write("---WORD COUNT---\n")
        f.write(f"Word Count : {df['Word Count'].sum()}\n")
        f.write(f"Word STD : {df['Word Count'].std()}\n")
        f.write(f"Word Count Tobi: {df[df['Names'] == 'Tobias Jungbluth']['Word Count'].sum()}\n")
        f.write(
            f"Word Count Tobi: {df[df['Names'] == 'Tobias Jungbluth']['Word Count'].sum()/df['Word Count'].sum() * 100}%\n")
        f.write(f"Word Count Lukas: {df[df['Names'] == 'Lukas']['Word Count'].sum()}\n")
        f.write(f"Word Count Lukas: {df[df['Names'] == 'Lukas']['Word Count'].sum()/df['Word Count'].sum() * 100}%\n")
        f.write(f"Word Count Mean: {df['Word Count'].mean()}\n")
        f.write(f"Word Count Tobi Mean: {df[df['Names'] == 'Tobias Jungbluth']['Word Count'].mean()}\n")
        f.write(f"Word Tobi STD : {df[df['Names'] == 'Tobias Jungbluth']['Word Count'].std()}\n")
        f.write(f"Word Count Lukas Mean: {df[df['Names'] == 'Lukas']['Word Count'].mean()}\n")
        f.write(f"Word Lukas STD : {df[df['Names'] == 'Lukas']['Word Count'].std()}\n")

        f.write("---WORD LENGTH---\n")
        f.write(f"Word Length : {df['Length'].sum()}\n")
        f.write(f"Word Length Tobi: {df[df['Names'] == 'Tobias Jungbluth']['Length'].sum()}\n")
        f.write(
            f"Word Length Tobi: {df[df['Names'] == 'Tobias Jungbluth']['Length'].sum()/df['Length'].sum() * 100}%\n")
        f.write(f"Word Length Lukas: {df[df['Names'] == 'Lukas']['Length'].sum()}\n")
        f.write(f"Word Length Lukas: {df[df['Names'] == 'Lukas']['Length'].sum()/df['Length'].sum() * 100}%\n")
        f.write(f"Word Length Mean: {df['Length'].mean()}\n")
        f.write(f"Word Length Tobi Mean: {df[df['Names'] == 'Tobias Jungbluth']['Length'].mean()}\n")
        f.write(f"Word Length Tobi STD: {df[df['Names'] == 'Tobias Jungbluth']['Length'].std()}\n")
        f.write(f"Word Length Lukas Mean: {df[df['Names'] == 'Lukas']['Length'].mean()}\n")
        f.write(f"Word Length Lukas STD: {df[df['Names'] == 'Lukas']['Length'].std()}\n")

        f.write("---MEDIA---\n")
        f.write(f"Non Media Messages: {df['Messages'].count()}\n")
        f.write(f"Non Media Messages: {df['Messages'].count()/df['Messages'].size*100}%\n")
        f.write(f"Media Messages: {df['Messages'].size - df['Messages'].count()}\n")
        f.write(f"Media Messages: {(df['Messages'].size - df['Messages'].count())/df['Messages'].size*100}%\n")
        f.write(f"Is Media Tobi: {df[(df['Media'] == True) & (df['Names'] == 'Tobias Jungbluth')]['Media'].count()}\n")
        f.write(f"Is Media Tobi: {df[(df['Media'] == True) & (df['Names'] == 'Tobias Jungbluth')]['Media'].count()/df[(df['Names'] == 'Tobias Jungbluth')]['Media'].count() *100}%\n")
        f.write(f"Is Not Media Tobi: {df[(df['Media'] == False) & (df['Names'] == 'Tobias Jungbluth')]['Media'].count()}\n")
        f.write(f"Is Not Media Tobi: {df[(df['Media'] == False) & (df['Names'] == 'Tobias Jungbluth')]['Media'].count() / df[df['Names'] == 'Tobias Jungbluth']['Media'].count() *100}%\n")
        f.write(f"Is Media Lukas: {df[(df['Media'] == True) & (df['Names'] == 'Lukas')]['Media'].count()}\n")
        f.write(f"Is Media Lukas: {df[(df['Media'] == True) & (df['Names'] == 'Lukas')]['Media'].count()/df[(df['Names'] == 'Lukas')]['Media'].count() *100}%\n")
        f.write(f"Is Not Media Lukas: {df[(df['Media'] == False) & (df['Names'] == 'Lukas')]['Media'].count()}\n")
        f.write(f"Is Not Media Lukas: {df[(df['Media'] == False) & (df['Names'] == 'Lukas')]['Media'].count() / df[df['Names'] == 'Lukas']['Media'].count() *100}%\n")

        f.write("---Time---\n")
        f.write(f"Number of unique days:\n {df['Day'].value_counts()}\n")
        corr_stuff = pandas.Series(data=range(1, 31 + 1), index=sorted(df['Day'].value_counts().index.values))
        f.write(f"Correlation between day count and ascend:\n {df['Day'].value_counts().corr(corr_stuff)}\n")
        f.write(f"Number of unique days of Lukas:\n {df[df['Names'] == 'Lukas']['Day'].value_counts()}\n")
        f.write(f"Number of unique days of Tobi:\n {df[df['Names'] == 'Tobias Jungbluth']['Day'].value_counts()}\n")
        f.write(f"Number of unique hours:\n {df['Hour'].value_counts()}\n")
        corr_stuff = pandas.Series(data=range(0, df['Hour'].value_counts().index.values.size), index=sorted(df['Hour'].value_counts().index.values))
        f.write(f"Correlation between hour count and ascend:\n {df['Hour'].value_counts().corr(corr_stuff)}\n")
        f.write(f"Number of unique hours of Lukas:\n {df[df['Names'] == 'Lukas']['Hour'].value_counts()}\n")
        f.write(f"Number of unique hours of Tobi:\n {df[df['Names'] == 'Tobias Jungbluth']['Hour'].value_counts()}\n")
        f.write(f"Number of unique minutes:\n {df['Minute'].value_counts()}\n")
        corr_stuff = pandas.Series(data=range(0, df['Minute'].value_counts().index.values.size),
                                   index=sorted(df['Minute'].value_counts().index.values))
        f.write(f"Number of unique minutes:\n {df['Minute'].value_counts().corr(corr_stuff)}\n")
        f.write(f"Number of unique minutes of Lukas:\n {df[df['Names'] == 'Lukas']['Minute'].value_counts()}\n")
        f.write(f"Number of unique minutes of Tobi:\n {df[df['Names'] == 'Tobias Jungbluth']['Minute'].value_counts()}\n")

        f.write("---WORDS---\n")
        f.write(f"Number of unique words: {df_words['Words'].nunique()}\n")
        f.write(f"Most Used words to 50: \n{df_words['Words'].value_counts()[:50]}\n")
        f.write(f"Most Used words 50 to 100: \n{df_words['Words'].value_counts()[50:100]}\n")
        f.write(f"Most Used words 100 to 150: \n{df_words['Words'].value_counts()[100:150]}\n")
        f.write(f"Most Used words 150 to 200: \n{df_words['Words'].value_counts()[150:200]}\n")

        f.write(f"Most Used words of Lukas to 50:      \n{df_words[df_words['Names'] == 'Lukas']['Words'].value_counts()[:50]}\n")
        f.write(f"Most Used words of Lukas 50 to 100:  \n{df_words[df_words['Names'] == 'Lukas']['Words'].value_counts()[50:100]}\n")
        f.write(f"Most Used words of Lukas 100 to 150: \n{df_words[df_words['Names'] == 'Lukas']['Words'].value_counts()[100:150]}\n")
        f.write(f"Most Used words of Lukas 150 to 200: \n{df_words[df_words['Names'] == 'Lukas']['Words'].value_counts()[150:200]}\n")

        f.write(f"Most Used words of Tobias to 50:      \n{df_words[df_words['Names'] == 'Tobias Jungbluth']['Words'].value_counts()[:50]}\n")
        f.write(f"Most Used words of Tobias 50 to 100:  \n{df_words[df_words['Names'] == 'Tobias Jungbluth']['Words'].value_counts()[50:100]}\n")
        f.write(f"Most Used words of Tobias 100 to 150: \n{df_words[df_words['Names'] == 'Tobias Jungbluth']['Words'].value_counts()[100:150]}\n")
        f.write(f"Most Used words of Tobias 150 to 200: \n{df_words[df_words['Names'] == 'Tobias Jungbluth']['Words'].value_counts()[150:200]}\n")



if __name__ == "__main__":
    out_put_analysis(*create_data_frame())
