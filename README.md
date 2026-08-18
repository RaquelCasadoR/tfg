# Machine Learning for Financial Time Series Prediction

Undergraduate thesis (TFG) project investigating whether machine learning models can
predict short-term price direction of major cryptocurrencies, and whether any predictive
edge found translates into a profitable trading strategy.

> The full written thesis (in Spanish) is available in [`Manual.pdf`](./Manual.pdf).

## Motivation

Financial time series are famously close to a random walk (Efficient Market Hypothesis).
This project asks three concrete questions:

1. Does a naive lag-based model already capture most of the predictable signal in crypto
   prices, or does adding engineered features help?
2. Do per-asset classification models trained with technical indicators, walk-forward
   validation, and hyperparameter tuning beat a random baseline?
3. Does pooling data across multiple assets into a single global model generalize better
   than training one model per asset?
4. If a model shows any edge, does it survive being turned into an actual trading strategy?

## Data

- **9 assets**: BTC, ETH, XRP, BNB, SOL, ADA, TRX, LINK, AVAX (vs. USDT, some also vs. BTC)
- **3 frequencies**: 1h, 4h, 1d candles
- **Range**: 2016-01-01 to 2025-01-01
- **Source**: Binance historical OHLC data

Raw CSVs are not tracked in this repository to keep it lightweight (~200MB of historical
price data). To reproduce the experiments, download the corresponding historical klines
for the symbols/frequencies above from the Binance API and place them under `Datos/`
following the naming convention `SYMBOL_FREQUENCY_01-01-2016_01-01-2025.csv`.

## Approach — four experiments

| # | Experiment | Code | Question |
|---|------------|------|----------|
| 1 | **Baseline** | `inicial.ipynb` / `mainINICIAL.py` | Can simple lagged prices (OLS, MLP regressor) predict the next price? Includes an Augmented Dickey-Fuller stationarity test. |
| 2 | **Per-asset "expert" models** | `characteristics.ipynb` / `mainCHARACT.py` | Do technical-indicator features + classification (MLP, Random Forest, Gradient Boosting) beat the baseline, at 1-day and 7-day horizons (`W1` / `W7`)? |
| 3 | **Global multi-asset model** | `global.ipynb` / `mainGLOBAL.py` | Does a single model trained across all assets jointly generalize better than one model per asset? |
| 4 | **Trading strategy backtest** | `trading_strategy.ipynb` | Do the model's signals produce a profitable strategy out-of-sample? |

## Key techniques

- Feature engineering with technical indicators (**TA-Lib**)
- **Walk-forward (rolling-origin) validation** to avoid look-ahead bias
- **Hyperparameter optimization** with **Optuna**
- Class-imbalance handling (`compute_sample_weight`)
- Parametrized, reproducible experiment orchestration via **papermill**

## Results (summary)

Across all four experiments, out-of-sample classification accuracy stayed close to
**50-52%**, only marginally above the random baseline. This is consistent with the
Efficient Market Hypothesis and the well-documented difficulty of predicting short-term
crypto price direction from price/technical data alone — the project treats this as a
meaningful (negative) result rather than a failure, and uses it to motivate the final
question tackled in `trading_strategy.ipynb`: whether such a modest statistical edge can
still be captured profitably once turned into an actual strategy. Full numeric results
per asset/frequency/model are in the `final_results_*.csv` files inside each experiment
folder, and are discussed in depth in the accompanying thesis (`Manual.pdf`).

## Tech stack

Python · pandas · scikit-learn · TA-Lib · Optuna · papermill · statsmodels · Matplotlib

## Project structure

```
.
├── Datos/                    # Raw price data (not tracked — see "Data" above)
├── INICIAL/                  # Results for Experiment 1
├── EXPERTO W1/, EXPERTO W7/  # Results for Experiment 2 (1-day / 7-day horizon)
├── GLOBAL W1/, GLOBAL W7/    # Results for Experiment 3 (1-day / 7-day horizon)
├── config.py                 # Shared experiment configuration (assets, frequencies, window)
├── inicial.ipynb             # Experiment 1 notebook
├── characteristics.ipynb     # Experiment 2 notebook
├── global.ipynb              # Experiment 3 notebook
├── trading_strategy.ipynb    # Experiment 4 notebook
├── mainINICIAL.py            # Orchestrates Experiment 1 across frequencies
├── mainCHARACT.py            # Orchestrates Experiment 2 across frequencies
├── mainGLOBAL.py             # Orchestrates Experiment 3 across frequencies
├── Manual.pdf                # Full written thesis (Spanish)
└── requirements.txt
```

## How to run

```bash
pip install -r requirements.txt

python mainINICIAL.py   # Experiment 1 — baseline lag models
python mainCHARACT.py   # Experiment 2 — per-asset expert models
python mainGLOBAL.py    # Experiment 3 — global multi-asset model
```

Then open `trading_strategy.ipynb` for Experiment 4.

## Limitations & future work

- Models rely solely on price-derived features; on-chain metrics or sentiment data could
  add signal beyond price action alone.
- The trading strategy backtest does not yet account for transaction costs and slippage
  at scale — a natural next step before treating results as tradable.
- Deep learning sequence models (LSTM/Transformer) were out of scope for this thesis but
  are a natural extension of the "global model" direction.

## Author

Raquel Casado — [add LinkedIn / contact here]
