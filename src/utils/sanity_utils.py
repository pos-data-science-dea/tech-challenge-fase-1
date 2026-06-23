import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def avalia_valores_nulos(df):
    tamanho_df = df.shape[0]
    df_nulos = df.isna().sum().to_frame().rename(columns={0: 'QTD_NULOS'})
    df_nulos['%_NULOS'] = df_nulos['QTD_NULOS']/tamanho_df
    
    return df_nulos

def avalia_valores_distintos(df):
    tamanho_df = df.shape[0]
    distinct_counts = df.nunique().to_frame().rename(columns={0: 'QTD_DISTINTOS'})
    distinct_counts['%_DISTINTOS'] = distinct_counts['QTD_DISTINTOS']/tamanho_df
    
    return distinct_counts

def avalia_duplicadas(df):
    return df.duplicated().sum()

def obter_tab_freq_abs(df, coluna):

    print("Tabela de frequencias")
    tam_df = df.shape[0]
    
    df = df[coluna].value_counts().to_frame()
    df.columns = ['freq_absoluta']
    df = df.freq_absoluta.value_counts().to_frame().reset_index().rename(columns={'index':'qtd_freq'})
    df['freq_relativa'] = round((df['freq_absoluta']/tam_df), 2)
    
    return df

def obter_tab_freq(df, coluna, n=15):
    print("Tabela de frequencias")
    tam_df = df.shape[0]
    
    df = df[coluna].value_counts(dropna=False).to_frame().reset_index()
    df.columns = [coluna,'freq_absoluta']
    df['freq_relativa'] = round((df['freq_absoluta']/tam_df), 2)
    
    return df.head(n)

def plota_histograma_e_boxplot(df, coluna, bins=30, kde=True):
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    
    # Histograma
    sns.histplot(                       
        df[coluna].dropna(),
        bins=bins,
        color="steelblue",
        edgecolor="white",
        kde=kde,                       
        ax=axes[0]
    )
    axes[0].set_title(f"Histograma - {coluna}")
    axes[0].set_ylabel("Frequência")
    axes[0].set_xlabel(f"{coluna}")
    
    # Boxplot
    sns.boxplot(data=df, y=coluna, ax=axes[1])
    axes[1].set_title(f"Boxplot - {coluna}")
    axes[1].axhline(df[coluna].mean(), color="red", linestyle="--", label="Média")
    axes[1].legend()
    
    sns.despine()
    plt.tight_layout()
    plt.show()    

def plota_bar(df, coluna):
    freq = df[coluna].value_counts(dropna=False).reset_index()
    freq.columns = [coluna, 'freq_absoluta']
    freq['freq_relativa'] = freq['freq_absoluta'] / df.shape[0]
    
    fig, ax = plt.subplots() 
    bars = ax.bar(freq[coluna].astype(str), freq['freq_absoluta'], color='steelblue', edgecolor='white')
    
    for bar, (_, row) in zip(bars, freq.iterrows()):
        ax.text(                                       
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + freq['freq_absoluta'].max() * 0.01,
            f"{int(row['freq_absoluta'])}\n({row['freq_relativa']:.1%})",
            ha='center', va='bottom', fontsize=9
        )
        
    ax.set_title(f"Distribuição da coluna {coluna}")   # ✅
    ax.set_xlabel(f"{coluna}")
    ax.set_ylabel('Frequência Absoluta')
    ax.set_ylim(0, freq['freq_absoluta'].max() * 1.2)
    sns.despine()
    plt.tight_layout()
    plt.show()   