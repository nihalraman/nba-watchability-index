import pandas as pd
from datetime import datetime

# Read the gamelog data
df = pd.read_csv('/Users/duncanl/projects/nba-watchability-index/data/gamelog_stats.csv')

# Convert Date to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Filter for 2024 games
df_2024 = df[df['Date'].dt.year == 2024].copy()

# Sort by player and date
df_2024 = df_2024.sort_values(['Player', 'Date'])

# Create a boolean mask for 20+ point games
df_2024['20_plus_points'] = df_2024['PTS'] >= 20

# Function to find streaks
def find_streaks(group):
    group = group.reset_index(drop=True)  # Reset index so we can safely use idx-4
    streak = 0
    streaks = []
    for idx, row in group.iterrows():
        if row['20_plus_points']:
            streak += 1
            if streak >= 10:
                streaks.append({
                    'start_date': group.loc[idx-4, 'Date'],
                    'end_date': row['Date'],
                    'games': streak
                })
        else:
            streak = 0
    return streaks


# Find streaks for each player
results = []
for player, group in df_2024.groupby('Player'):
    streaks = find_streaks(group)
    for streak in streaks:
        results.append({
            'player': player,
            'start_date': streak['start_date'],
            'end_date': streak['end_date'],
            'games': streak['games']
        })

# Convert results to DataFrame and sort by streak length
results_df = pd.DataFrame(results)
if not results_df.empty:
    results_df = results_df.sort_values('games', ascending=False)
    print("\nPlayers with 5+ consecutive 20+ point games in 2024:")
    for _, row in results_df.iterrows():
        print(f"\n{row['player']}")
        print(f"Streak: {row['games']} games")
        print(f"From: {row['start_date'].strftime('%Y-%m-%d')} to {row['end_date'].strftime('%Y-%m-%d')}")
else:
    print("No players found with 5+ consecutive 20+ point games in 2024.") 