from flask import Flask, request, jsonify, redirect, url_for
import mysql.connector as mysql
import bcrypt
from datetime import datetime, timedelta, date

class StudentTable:
    def __init__(self):
        self.db = mysql.connect(
        host="79.171.148.163",
        user="user",
        passwd="MaaGodt*7913!",
        database="LogunitDB"
        )
        self.mycursor = self.db.cursor(dictionary=True)

        print("connected to database")
        

    def calculate_days(self, uddannelses_Hold_ID):
        query = """
        SELECT navn, opstartsDato
        FROM Students
        WHERE uddannelseID = %s
        """
        self.mycursor.execute(query, (uddannelses_Hold_ID,))
        results = self.mycursor.fetchall()
        
        if not results:
            return []
        
        today = datetime.now().date()
        days_diff_list = []
        
        for result in results:
            navn = result['navn']
            start_date = result['opstartsDato']  # Already a date object
            
            # Calculate weekdays difference
            days_difference = self.count_weekdays(start_date, today)
            
            days_diff_list.append({'navn': navn, 'days_difference': days_difference})
        
        return days_diff_list

    def count_weekdays(self, start_date, end_date):
        # Ensure start_date is before end_date
        if start_date > end_date:
            return 0
        
        weekdays_count = 0
        
        # Loop through each day from start_date to end_date
        while start_date <= end_date:
            # Check if start_date is a weekday (Monday to Friday)
            if start_date.weekday() < 5:
                weekdays_count += 1
            
            # Move to the next day
            start_date += timedelta(days=1)
        
        return weekdays_count

    def amount_Of_Checkins(self, uddannelses_Hold_ID):
        query = """
        SELECT s.navn, COUNT(c.studentID) AS antal
        FROM Students s
        LEFT JOIN Checkind c ON s.studentID = c.studentID
        WHERE s.uddannelseID = %s
        GROUP BY s.studentID, s.navn
        """
        self.mycursor.execute(query, (uddannelses_Hold_ID,))
        result = self.mycursor.fetchall()
        
        # Convert the result to the desired dictionary format
        checkin_counts = [{'navn': row['navn'], 'antal': row['antal']} for row in result]
        
        return checkin_counts

    def calc_attendance(self, checkin_counts, days_difference):
        if not days_difference:
            return {}

        # Create a dictionary from days_difference for quick lookup
        days_diff_dict = {entry['navn']: entry['days_difference'] for entry in days_difference}

        # Create a dictionary for check-in counts for quick lookup, defaulting to 0 if not found
        checkin_counts_dict = {entry['navn']: entry['antal'] for entry in checkin_counts}

        calced_attendance = {}
        for navn, days_diff in days_diff_dict.items():
            antal = checkin_counts_dict.get(navn, 0)  # Default to 0 if not found in checkin_counts
            diff_procent = (days_diff - antal) / days_diff * 100
            diff_procent=float("{:.2f}".format(diff_procent))
            calced_attendance[navn] = diff_procent

        return calced_attendance

    def checkedin_today(self, uddannelses_Hold_ID):
        # Get today's date
        today_date = datetime.now().date()
        
        # Query to check if each student has checked in today
        query = """
        SELECT s.navn, CASE WHEN COUNT(c.checkin) > 0 THEN TRUE ELSE FALSE END AS checked_in_today
        FROM Students s
        LEFT JOIN Checkind c ON s.studentID = c.studentID AND DATE(c.checkin) = %s
        WHERE s.uddannelseID = %s
        GROUP BY s.navn
        """
        
        self.mycursor.execute(query, (today_date, uddannelses_Hold_ID))
        result = self.mycursor.fetchall()
        
        # Create a dictionary to store checked-in status for each student
        checked_in_today = {entry['navn']: entry['checked_in_today'] for entry in result}
        
        return checked_in_today

    def get_attend_table(self, uddannelses_Hold_ID):
        # Calculate the days difference for students in the educational group
        days_diff_list = self.calculate_days(uddannelses_Hold_ID)
        
        # Get the number of check-ins for students in the educational group
        checkin_counts = self.amount_Of_Checkins(uddannelses_Hold_ID)
        
        # Calculate attendance difference percentage
        calced_attendance = self.calc_attendance(checkin_counts, days_diff_list)
        
        # Check if students have checked in today
        checks = self.checkedin_today(uddannelses_Hold_ID)
        
        # Combine all data into a single dictionary
        attendance_table = []
        for student in days_diff_list:
            navn = student['navn']
            days_difference = student['days_difference']
            attendance_percentage = calced_attendance.get(navn, 100.0)  # Default to 100% if not found
            checked_in_today = checks.get(navn, False)  # Default to False if not found
            attendance_table.append({
                'navn': navn,
                'attendance_percentage': attendance_percentage,
                'checked_in_today': checked_in_today
            })
        
        return attendance_table

# Example usage
if __name__ == "__main__":
    table = StudentTable()
    uddannelses_Hold_ID = 1  # Replace with the desired educational group ID
    
    # Get the attendance table
    attendance_table = table.get_attend_table(1)
    
    # Print the attendance table
    print("Attendance Table:")
    for entry in attendance_table:
        print(entry)
    
    
    