import pandas as pd
import streamlit as st
import plotly.express as px

df_fighter_result = pd.read_csv(r'D:\Workplace\.SPRING2025\DAP391m\EDA\fight_results_with_locale.csv') 
df_fight_stats = pd.read_csv(r'D:\Workplace\.SPRING2025\DAP391m\EDA\fight_stats_with_weghtclass_date_location.csv')
df_fighters = pd.read_csv(r'D:\Workplace\.SPRING2025\DAP391m\EDA\fighters_processed.csv')

# Sidebar navigation
section = st.sidebar.radio("Select Section", ["Fighter Overview", "Compare Fighters", "Matches Highlights"])

if section == "Fighter Overview":
    st.title("MMA Fighter")
    fighter_list = df_fighters["Name"].unique()
    selected_fighter = st.selectbox("Fighter:", fighter_list)

    fighter_info = df_fighters[df_fighters["Name"] == selected_fighter]

    if not fighter_info.empty:
        st.subheader("General:")
        st.write(f"**Name:** {selected_fighter}")

        nickname = fighter_info['Nickname'].values[0] if pd.notna(fighter_info['Nickname'].values[0]) else "N/A"
        st.write(f"**Nickname:** {nickname}")

        df_fighter_result["FIGHTER_1"] = df_fighter_result["FIGHTER_1"].str.lower()
        df_fighter_result["FIGHTER_2"] = df_fighter_result["FIGHTER_2"].str.lower()

        selected_fighter_lower = selected_fighter.lower()

        fighter_weight_history = df_fighter_result[
            (df_fighter_result["FIGHTER_1"] == selected_fighter_lower) | (df_fighter_result["FIGHTER_2"] == selected_fighter_lower)
        ]

        if fighter_weight_history.empty:
            st.write("No fight history available for this fighter.")
        else:
            fighter_weight_counts = fighter_weight_history.groupby("weight_class").size().reset_index(name="Total Fights")

            if len(fighter_weight_counts) == 1:
                weight_class = fighter_weight_counts["weight_class"].values[0] + " (1)"
                st.write(f"**Weight Class:** {weight_class}")
            else:
                st.subheader("Weight Class History")
                if not fighter_weight_counts.empty:
                    fig_weight_class = px.bar(
                        fighter_weight_counts,
                        x="weight_class",
                        y="Total Fights",
                        labels={"weight_class": "Weight Class", "Total Fights": "Number of Fights"},
                        text_auto=True
                    )
                    st.plotly_chart(fig_weight_class)

        wins = fighter_info["Wins"].values[0] if pd.notna(fighter_info["Wins"].values[0]) else 0
        losses = fighter_info["Losses"].values[0] if pd.notna(fighter_info["Losses"].values[0]) else 0
        draws = fighter_info["Draws"].values[0] if pd.notna(fighter_info["Draws"].values[0]) else 0
        total_fights = wins + losses + draws

        st.subheader("Fighting Records:")
        st.write(f"**Total:** {total_fights}")
        st.write(f"**Wins:** {wins}")
        st.write(f"**Losses:** {losses}")
        st.write(f"**Draws:** {draws}")

        st.subheader("Wins by method:")
        win_methods = {
            "KO/TKO": fighter_info["Win_by_KO/TKO_Percent"].values[0] if pd.notna(fighter_info["Win_by_KO/TKO_Percent"].values[0]) else 0,
            "Submission": fighter_info["Win_by_Submission_Percent"].values[0] if pd.notna(fighter_info["Win_by_Submission_Percent"].values[0]) else 0,
            "Decision": fighter_info["Win_by_Decision_Percent"].values[0] if pd.notna(fighter_info["Win_by_Decision_Percent"].values[0]) else 0
        }
        st.bar_chart(win_methods)

        striking_accuracy = fighter_info['Striking_Accuracy'].values[0]
        takedown_accuracy = fighter_info['Takedown_Accuracy'].values[0]
        striking_defense = fighter_info['Sig_Str_Def'].values[0]
        takedown_defense = fighter_info['Takedown_Def'].values[0]
        knockdown_avg = fighter_info['Knockdown_Avg'].values[0]
        submission_avg = fighter_info['Sub_Avg_Per_Min'].values[0]

        stats = {
            "Metrics": ["Striking Accuracy", "Takedown Accuracy", "Strike Defense", "Takedown Defense", "Knockdown Avg", "Submission Avg"],
            "Value": [striking_accuracy, takedown_accuracy, striking_defense, takedown_defense, knockdown_avg, submission_avg]
        }
        
        df_radar = pd.DataFrame(stats)

        fig = px.line_polar(df_radar, r="Value", theta="Metrics", line_close=True, markers=True)
        fig.update_traces(fill="toself", line=dict(color="blue"))

        st.subheader("Fighter Performance Overview")
        st.plotly_chart(fig)

    else:
        st.warning("No information found for this fighter.")
  
  
elif section == "Compare Fighters":
    st.title("Compare Fighters")

    fighter_list = df_fighters["Name"].unique()

    col1, col2 = st.columns(2)
    with col1:
        fighter_1 = st.selectbox("Select Fighter 1", fighter_list, key="fighter1")
    with col2:
        fighter_2 = st.selectbox("Select Fighter 2", fighter_list, key="fighter2")

    fighter_info_1 = df_fighters[df_fighters["Name"] == fighter_1]
    fighter_info_2 = df_fighters[df_fighters["Name"] == fighter_2]

    if not fighter_info_1.empty and not fighter_info_2.empty:
        # Chuẩn hóa tên võ sĩ
        fighter_1_clean = fighter_1.strip().lower()
        fighter_2_clean = fighter_2.strip().lower()

        df_fighter_result["FIGHTER_1"] = df_fighter_result["FIGHTER_1"].str.strip().str.lower()
        df_fighter_result["FIGHTER_2"] = df_fighter_result["FIGHTER_2"].str.strip().str.lower()

        # Lọc dữ liệu trận đấu của từng võ sĩ
        fighter_1_fights = df_fighter_result[
            (df_fighter_result["FIGHTER_1"] == fighter_1_clean) | (df_fighter_result["FIGHTER_2"] == fighter_1_clean)
        ]
        fighter_2_fights = df_fighter_result[
            (df_fighter_result["FIGHTER_1"] == fighter_2_clean) | (df_fighter_result["FIGHTER_2"] == fighter_2_clean)
        ]

        def get_top_location_and_winrate(fighter_name, fighter_fights):
            """Tìm địa điểm thi đấu nhiều nhất và tỷ lệ thắng của võ sĩ tại địa điểm đó"""
            if fighter_fights.empty:
                return "No data", "No fight data"

            top_location = fighter_fights["LOCATION"].mode().iloc[0]  # Địa điểm xuất hiện nhiều nhất

            # Tính số trận thắng tại địa điểm đó
            fights_at_top_location = fighter_fights[fighter_fights["LOCATION"] == top_location]
            wins = (
                (fights_at_top_location["FIGHTER_1"] == fighter_name) & (fights_at_top_location["fighter_1_result"] == 1)
            ) | (
                (fights_at_top_location["FIGHTER_2"] == fighter_name) & (fights_at_top_location["fighter_2_result"] == 1)
            )
            win_rate = wins.sum() / len(fights_at_top_location) if len(fights_at_top_location) > 0 else 0

            return top_location, f"{win_rate:.1%}"

        top_location_1, win_rate_1 = get_top_location_and_winrate(fighter_1_clean, fighter_1_fights)
        top_location_2, win_rate_2 = get_top_location_and_winrate(fighter_2_clean, fighter_2_fights)

        # Hiển thị dữ liệu
        st.subheader("Top Fighting Location & Win Rate")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"Most Fights Location: **{top_location_1}**")
            st.write(f"Win Rate at Location: **{win_rate_1}**")

        with col2:
            st.write(f"Most Fights Location: **{top_location_2}**")
            st.write(f"Win Rate at Location: **{win_rate_2}**")

        # So sánh các chỉ số chiến đấu
        metrics = ["Striking Accuracy", "Takedown Accuracy", "Strike Defense", "Takedown Defense", "Knockdown Avg", "Submission Avg"]
        values_1 = [
            fighter_info_1['Striking_Accuracy'].values[0],
            fighter_info_1['Takedown_Accuracy'].values[0],
            fighter_info_1['Sig_Str_Def'].values[0],
            fighter_info_1['Takedown_Def'].values[0],
            fighter_info_1['Knockdown_Avg'].values[0],
            fighter_info_1['Sub_Avg_Per_Min'].values[0]
        ]
        values_2 = [
            fighter_info_2['Striking_Accuracy'].values[0],
            fighter_info_2['Takedown_Accuracy'].values[0],
            fighter_info_2['Sig_Str_Def'].values[0],
            fighter_info_2['Takedown_Def'].values[0],
            fighter_info_2['Knockdown_Avg'].values[0],
            fighter_info_2['Sub_Avg_Per_Min'].values[0]
        ]

        df_compare = pd.DataFrame({
            "Metrics": metrics,
            fighter_1: values_1,
            fighter_2: values_2
        })

        st.subheader("fighter Stats Comparison")
        st.dataframe(df_compare)

        df_melted = df_compare.melt(id_vars=["Metrics"], var_name="Fighter", value_name="Value")

        fig = px.line_polar(df_melted, r="Value", theta="Metrics", color="Fighter", line_close=True, markers=True)
        fig.update_traces(fill="toself", line=dict(width=2))

        st.plotly_chart(fig)

    else:
        st.warning("No information found for one or both fighters.")


elif section == "Matches Highlights":
    st.title('Matches Highlight')

    # Danh sách các trận đấu
    matches_list = df_fighter_result["BOUT"].unique()
    selected_match = st.selectbox("Match:", matches_list)

    # Lọc thông tin trận đấu
    match_info = df_fighter_result[df_fighter_result["BOUT"] == selected_match]

    if not match_info.empty:
        # Lấy thông tin cơ bản của trận đấu
        match_weight_class = match_info["weight_class"].values[0]
        round_num = match_info["ROUND"].values[0]
        time = match_info["TIME"].values[0]
        total_round = match_info["Total_Rounds_Format"].values[0]

        st.subheader("Match highlight:")
        st.write(f"**Weight class:** {match_weight_class}")
        st.write(f"**Round:** {round_num}")
        st.write(f"**Time (minutes):** {time}")
        st.write(f"**Total Rounds:** {total_round}")

        # **Lấy tên hai võ sĩ trong trận đấu**
        fighter_1 = match_info["FIGHTER_1"].values[0].strip().lower()
        fighter_2 = match_info["FIGHTER_2"].values[0].strip().lower()

        # **Lọc dữ liệu võ sĩ từ df_fighters**
        fighter_info_1 = df_fighters[df_fighters["Name"].str.strip().str.lower() == fighter_1]
        fighter_info_2 = df_fighters[df_fighters["Name"].str.strip().str.lower() == fighter_2]

        # Nếu tìm thấy cả hai võ sĩ, tiến hành so sánh
        if not fighter_info_1.empty and not fighter_info_2.empty:
            st.subheader(f"Stats comparison")

            metrics = ["Striking Accuracy", "Takedown Accuracy", "Strike Defense", "Takedown Defense", "Knockdown Avg", "Submission Avg"]
            values_1 = [
                fighter_info_1['Striking_Accuracy'].values[0],
                fighter_info_1['Takedown_Accuracy'].values[0],
                fighter_info_1['Sig_Str_Def'].values[0],
                fighter_info_1['Takedown_Def'].values[0],
                fighter_info_1['Knockdown_Avg'].values[0],
                fighter_info_1['Sub_Avg_Per_Min'].values[0]
            ]
            values_2 = [
                fighter_info_2['Striking_Accuracy'].values[0],
                fighter_info_2['Takedown_Accuracy'].values[0],
                fighter_info_2['Sig_Str_Def'].values[0],
                fighter_info_2['Takedown_Def'].values[0],
                fighter_info_2['Knockdown_Avg'].values[0],
                fighter_info_2['Sub_Avg_Per_Min'].values[0]
            ]

            df_compare = pd.DataFrame({
                "Metrics": metrics,
                fighter_1.title(): values_1,
                fighter_2.title(): values_2
            })
            st.dataframe(df_compare)

            df_melted = df_compare.melt(id_vars=["Metrics"], var_name="Fighter", value_name="Value")
            fig = px.line_polar(df_melted, r="Value", theta="Metrics", color="Fighter", line_close=True, markers=True)
            fig.update_traces(fill="toself", line=dict(width=2))
            st.plotly_chart(fig)

        else:
            st.warning("No information found for one or both fighters.")
    else:
        st.warning("No match information found.")





