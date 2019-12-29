def strip_df_column(df_column):

    df_column = df_column.map(lambda x: x.strip())

    return df_column
