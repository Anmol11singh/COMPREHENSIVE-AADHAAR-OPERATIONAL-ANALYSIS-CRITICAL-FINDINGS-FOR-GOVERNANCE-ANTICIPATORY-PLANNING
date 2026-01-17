import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

print("=" * 90)
print("TIME SERIES FORECASTING: EXPONENTIAL SMOOTHING & SIMPLE FORECAST MODELS")
print("=" * 90)

# Prepare daily time series data for forecasting
forecast_data = daily_trends.copy()
forecast_data = forecast_data.sort_values('Date').reset_index(drop=True)
forecast_data['total_operations'] = forecast_data['total_operations'].fillna(0)

# Split into train and test (last 7 days for validation)
train_size = len(forecast_data) - 7
train_data = forecast_data.iloc[:train_size].copy()
test_data = forecast_data.iloc[train_size:].copy()

print(f"\n📊 DATA PREPARATION:")
print(f"  Total observations: {len(forecast_data)}")
print(f"  Training set: {len(train_data)} days")
print(f"  Test set: {len(test_data)} days")
print(f"  Forecast horizon: 14 days")

# Exponential Smoothing Model
print(f"\n" + "=" * 90)
print("EXPONENTIAL SMOOTHING FORECASTING MODEL")
print("=" * 90)

print(f"\n🔧 MODEL ASSUMPTIONS:")
print(f"  - Recent observations have more weight than older ones")
print(f"  - Trend component follows linear or damped exponential pattern")
print(f"  - Seasonality can be additive or multiplicative")
print(f"  - Forecast uncertainty increases with horizon")

# Simple exponential smoothing with trend
from scipy.ndimage import uniform_filter1d

# Calculate smoothing parameters
alpha = 0.3  # Level smoothing
beta = 0.1   # Trend smoothing

train_values = train_data['total_operations'].values
smoothed_level = [train_values[0]]
smoothed_trend = [0]

for _smooth_i in range(1, len(train_values)):
    level = alpha * train_values[_smooth_i] + (1 - alpha) * (smoothed_level[-1] + smoothed_trend[-1])
    trend = beta * (level - smoothed_level[-1]) + (1 - beta) * smoothed_trend[-1]
    smoothed_level.append(level)
    smoothed_trend.append(trend)

# Generate forecasts
forecast_steps = len(test_data) + 14
exp_forecast = []
for h in range(1, forecast_steps + 1):
    forecast_value = smoothed_level[-1] + h * smoothed_trend[-1]
    exp_forecast.append(max(0, forecast_value))  # Ensure non-negative

exp_forecast = np.array(exp_forecast)

# Calculate residuals for confidence intervals
train_fitted = np.array([smoothed_level[_fit_i] for _fit_i in range(len(train_values))])
residuals = train_values - train_fitted
residual_std = np.std(residuals)

# Confidence intervals (widen with forecast horizon)
exp_lower_95 = []
exp_upper_95 = []
for h in range(1, forecast_steps + 1):
    margin = 1.96 * residual_std * np.sqrt(1 + (h / len(train_data)))
    exp_lower_95.append(max(0, exp_forecast[h-1] - margin))
    exp_upper_95.append(exp_forecast[h-1] + margin)

# Evaluate on test set
test_exp_pred = exp_forecast[:len(test_data)]
test_actual = test_data['total_operations'].values

mae_exp = np.mean(np.abs(test_actual - test_exp_pred))
rmse_exp = np.sqrt(np.mean((test_actual - test_exp_pred)**2))
mape_exp = np.mean(np.abs((test_actual - test_exp_pred) / (test_actual + 1))) * 100

print(f"\n📊 EXPONENTIAL SMOOTHING VALIDATION (Test Set):")
print(f"  Smoothing parameters: α={alpha}, β={beta}")
print(f"  Mean Absolute Error (MAE): {mae_exp:,.0f} operations")
print(f"  Root Mean Squared Error (RMSE): {rmse_exp:,.0f} operations")
print(f"  Mean Absolute Percentage Error (MAPE): {mape_exp:.2f}%")

# Generate future dates
last_date = forecast_data['Date'].max()
future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=14, freq='D')
all_forecast_dates = pd.concat([
    test_data['Date'].reset_index(drop=True),
    pd.Series(future_dates, name='Date')
], ignore_index=True)

exp_forecast_df = pd.DataFrame({
    'date': all_forecast_dates,
    'forecast': exp_forecast,
    'lower_95': exp_lower_95,
    'upper_95': exp_upper_95
})

print(f"\n📅 EXPONENTIAL SMOOTHING 14-DAY FORECAST:")
future_exp = exp_forecast_df.iloc[-14:]
for _, row in future_exp.head(7).iterrows():
    print(f"  {row['date'].strftime('%Y-%m-%d')}: {row['forecast']:,.0f} ops (95% CI: [{row['lower_95']:,.0f}, {row['upper_95']:,.0f}])")
print(f"  ... (showing first 7 days)")

# Moving Average Model
print(f"\n" + "=" * 90)
print("MOVING AVERAGE FORECASTING MODEL")
print("=" * 90)

print(f"\n🔧 MODEL ASSUMPTIONS:")
print(f"  - Recent average represents expected near-term behavior")
print(f"  - No strong trend or seasonality components")
print(f"  - Mean-reverting process")
print(f"  - Suitable for stable operational patterns")

# Calculate 7-day and 14-day moving averages
ma_7 = train_data['total_operations'].rolling(window=7, min_periods=1).mean().iloc[-1]
ma_14 = train_data['total_operations'].rolling(window=14, min_periods=1).mean().iloc[-1]
ma_21 = train_data['total_operations'].rolling(window=21, min_periods=1).mean().iloc[-1]

# Use weighted average of different windows
ma_forecast_value = 0.5 * ma_7 + 0.3 * ma_14 + 0.2 * ma_21
ma_forecast = np.full(forecast_steps, ma_forecast_value)

# Confidence intervals based on recent volatility
recent_std = train_data['total_operations'].tail(14).std()
ma_lower_95 = np.maximum(0, ma_forecast - 1.96 * recent_std)
ma_upper_95 = ma_forecast + 1.96 * recent_std

# Evaluate on test set
test_ma_pred = ma_forecast[:len(test_data)]

mae_ma = np.mean(np.abs(test_actual - test_ma_pred))
rmse_ma = np.sqrt(np.mean((test_actual - test_ma_pred)**2))
mape_ma = np.mean(np.abs((test_actual - test_ma_pred) / (test_actual + 1))) * 100

print(f"\n📊 MOVING AVERAGE VALIDATION (Test Set):")
print(f"  MA windows: 7-day (50%), 14-day (30%), 21-day (20%)")
print(f"  Mean Absolute Error (MAE): {mae_ma:,.0f} operations")
print(f"  Root Mean Squared Error (RMSE): {rmse_ma:,.0f} operations")
print(f"  Mean Absolute Percentage Error (MAPE): {mape_ma:.2f}%")

ma_forecast_df = pd.DataFrame({
    'date': all_forecast_dates,
    'forecast': ma_forecast,
    'lower_95': ma_lower_95,
    'upper_95': ma_upper_95
})

print(f"\n📅 MOVING AVERAGE 14-DAY FORECAST:")
future_ma = ma_forecast_df.iloc[-14:]
for _, row in future_ma.head(7).iterrows():
    print(f"  {row['date'].strftime('%Y-%m-%d')}: {row['forecast']:,.0f} ops (95% CI: [{row['lower_95']:,.0f}, {row['upper_95']:,.0f}])")
print(f"  ... (showing first 7 days)")

# Model Comparison
print(f"\n" + "=" * 90)
print("MODEL COMPARISON & RECOMMENDATIONS")
print("=" * 90)

print(f"\n📊 TEST SET PERFORMANCE COMPARISON:")
print(f"\n  {'Metric':<30} {'Exp Smoothing':<20} {'Moving Avg':<20}")
print(f"  {'-'*70}")
print(f"  {'MAE (operations)':<30} {mae_exp:>15,.0f}    {mae_ma:>15,.0f}")
print(f"  {'RMSE (operations)':<30} {rmse_exp:>15,.0f}    {rmse_ma:>15,.0f}")
print(f"  {'MAPE (%)':<30} {mape_exp:>15.2f}%   {mape_ma:>15.2f}%")

best_model = "Exponential Smoothing" if mape_exp < mape_ma else "Moving Average"
print(f"\n✅ RECOMMENDED MODEL: {best_model}")
print(f"   Lower MAPE indicates better percentage accuracy on test set")

# Ensemble Forecast (average of both models)
ensemble_forecast = (exp_forecast_df.set_index('date')['forecast'] + ma_forecast_df.set_index('date')['forecast']) / 2
ensemble_lower = (exp_forecast_df.set_index('date')['lower_95'] + ma_forecast_df.set_index('date')['lower_95']) / 2
ensemble_upper = (exp_forecast_df.set_index('date')['upper_95'] + ma_forecast_df.set_index('date')['upper_95']) / 2

ensemble_df = pd.DataFrame({
    'date': future_dates,
    'forecast': ensemble_forecast.values[-14:],
    'lower_95': ensemble_lower.values[-14:],
    'upper_95': ensemble_upper.values[-14:]
})

print(f"\n📊 ENSEMBLE FORECAST (Average of Exp Smoothing & Moving Average):")
for _, row in ensemble_df.head(7).iterrows():
    print(f"  {row['date'].strftime('%Y-%m-%d')}: {row['forecast']:,.0f} ops (95% CI: [{row['lower_95']:,.0f}, {row['upper_95']:,.0f}])")
print(f"  ... (showing first 7 days)")

# Summary statistics
avg_forecast = ensemble_df['forecast'].mean()
forecast_range = ensemble_df['forecast'].max() - ensemble_df['forecast'].min()
avg_ci_width = (ensemble_df['upper_95'] - ensemble_df['lower_95']).mean()

print(f"\n📈 FORECAST SUMMARY:")
print(f"  Average daily forecast (14 days): {avg_forecast:,.0f} operations")
print(f"  Forecast range: {forecast_range:,.0f} operations")
print(f"  Average 95% CI width: {avg_ci_width:,.0f} operations")
print(f"  Forecast stability: {'High' if forecast_range < avg_forecast * 0.1 else 'Moderate' if forecast_range < avg_forecast * 0.3 else 'Variable'}")

print(f"\n✅ Forecasting models developed and validated")
print(f"   - Exponential smoothing with trend component")
print(f"   - Weighted moving average baseline")
print(f"   - 95% confidence intervals provided for uncertainty quantification")
print(f"   - Ensemble approach combines model strengths")
