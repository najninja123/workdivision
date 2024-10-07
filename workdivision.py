import streamlit as st
import pandas as pd

# Define group members and tasks
group_members = ['Najneen', 'Radhika', 'Shreya', 'Ankush', 'Ayushi']
tasks = ['Data Management', 'Analysis', 'Key Findings and Recommendations', 'Report Writing', 'Presentation Writing']

# Initialize session state to track inputs
if 'task_data' not in st.session_state:
    st.session_state.task_data = {member: {task: {person: 0 for person in group_members} for task in tasks} for member in group_members}

if 'submitted_members' not in st.session_state:
    st.session_state.submitted_members = []

# Get the current user input
st.title("Group Task Contribution App")
st.write("Please enter your name to start assigning contributions.")
user_name = st.selectbox("Select your name", group_members)

if user_name not in st.session_state.submitted_members:
    st.write(f"Hello, {user_name}. Please enter the contribution percentages for each task.")
    
    with st.form("task_contributions"):
        task_data = st.session_state.task_data[user_name]

        # Input for each task and each group member
        for task in tasks:
            st.subheader(f"Task: {task}")
            total_percentage = 0
            for person in group_members:
                task_data[task][person] = st.number_input(
                    f"{person}'s contribution for {task}", min_value=0, max_value=100, key=f"{user_name}_{task}_{person}"
                )
                total_percentage += task_data[task][person]
            
            # Validation to ensure each task's total is 100%
            if total_percentage != 100:
                st.error(f"The total for {task} must equal 100%. Current total: {total_percentage}%")
        
        # Submit button
        submitted = st.form_submit_button("Submit")

    if submitted and total_percentage == 100:
        st.success(f"Thank you, {user_name}. Your contributions have been recorded.")
        st.session_state.submitted_members.append(user_name)
else:
    st.info(f"{user_name}, you have already submitted your contributions.")

# Output the final report after all members have submitted their inputs
if len(st.session_state.submitted_members) == len(group_members):
    st.subheader("Final Weighted Contributions Report")

    # Calculate weighted contributions
    final_data = {task: {person: 0 for person in group_members} for task in tasks}

    for task in tasks:
        for person in group_members:
            # Self-assessment weighting (40%)
            self_contrib = st.session_state.task_data[person][task][person] * 0.4
            
            # Peer assessments (60%)
            peer_contrib = sum(st.session_state.task_data[other][task][person] for other in group_members if other != person) * 0.6 / (len(group_members) - 1)
            
            # Final weighted contribution
            final_data[task][person] = round(self_contrib + peer_contrib, 2)

    # Display the final data as a DataFrame
    final_df = pd.DataFrame(final_data)
    st.dataframe(final_df)

    # Provide a download option for the report
    st.download_button(label="Download Final Report", data=final_df.to_csv().encode('utf-8'), file_name='final_contributions_report.csv', mime='text/csv')

else:
    st.warning("Waiting for all group members to submit their contributions before generating the final report.")
