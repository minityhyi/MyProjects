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
        
    def get_Students_From_Checkin(self,uddannelses_Hold_ID):
        query = """
        SELECT DISTINCT s.studentID, s.navn
        FROM Checkind c
        JOIN Students s ON c.studentID = s.studentID
        WHERE s.uddannelseID = %s
        """
        self.mycursor.execute(query, (uddannelses_Hold_ID,))
        result = self.mycursor.fetchall()
        
        names = [row['navn'] for row in result]
        
        return names
        
    def amount_Of_Checkins(self, uddannelses_Hold_ID):
        query = """
        SELECT s.navn, COUNT(c.studentID) AS antal
        FROM Checkind c
        JOIN Students s ON c.studentID = s.studentID
        WHERE s.uddannelseID = %s
        GROUP BY s.studentID, s.navn
        """
        self.mycursor.execute(query, (uddannelses_Hold_ID,))
        result = self.mycursor.fetchall()
        
        # Convert the result to the desired dictionary format
        checkin_counts = [{'navn': row['navn'], 'antal': row['antal']} for row in result]
        
        return checkin_counts
    
    def calculate_Days(self, studentID):
        query = """
        SELECT opstartsDato
        FROM Students
        WHERE studentID = %s
        """
        self.mycursor.execute(query, (studentID,))
        result = self.mycursor.fetchone()
        
        if not result:
            return None
        
        start_date = result['opstartsDato']  # Already a date object
        today = datetime.now().date()
        
        # Calculate weekdays difference
        days_difference = self.count_Weekdays(start_date, today)
        
        return days_difference

    def count_Weekdays(self, start_date, current_date):
        # Ensure start_date is before current_date
        if start_date > current_date:
            return 0
        
        weekdays_count = 0
        
        # Loop through each day from start_date to current_date
        while start_date <= current_date:
            # Check if start_date is a weekday (Monday to Friday)
            if start_date.weekday() < 5:
                weekdays_count += 1
            
            # Move to the next day
            start_date += timedelta(days=1)
        
        return weekdays_count
    
    def calc_attendance(self, checkin_counts, days_difference):
        if not checkin_counts:
            return {}
        
        navne = [entry['navn'] for entry in checkin_counts]
        antal = [entry['antal'] for entry in checkin_counts]
        
        diff_Procent_List = [(days_difference - x) / days_difference * 100 for x in antal]
        
        calced_attendance = dict(zip(navne, diff_Procent_List))
        
        return calced_attendance
    
    def checkedin_today(self, uddannelses_Hold_ID):
        # Get today's date
        today_date = date.today()
        
        # Query to get all students and their check-in status for today
        query = """
        SELECT s.studentID, 
               CASE WHEN COUNT(c.checkin) > 0 THEN TRUE ELSE FALSE END AS checked_in_today
        FROM Students s
        LEFT JOIN Checkind c ON s.studentID = c.studentID AND DATE(c.checkin) = %s
        WHERE s.uddannelseID = %s
        GROUP BY s.studentID
        """
        
        self.mycursor.execute(query, (today_date, uddannelses_Hold_ID))
        result = self.mycursor.fetchall()
        
        # Create a dictionary to store checked-in status for each student
        checked_in_today = {entry['studentID']: entry['checked_in_today'] for entry in result}
        
        # Include students who haven't checked in today with False status
        # Fetch all students in the educational group
        query_all_students = """
        SELECT studentID
        FROM Students
        WHERE uddannelseID = %s
        """
        self.mycursor.execute(query_all_students, (uddannelses_Hold_ID,))
        all_students = self.mycursor.fetchall()
        
        # Update checked_in_today dictionary with students who haven't checked in today
        for student in all_students:
            student_id = student['studentID']
            if student_id not in checked_in_today:
                checked_in_today[student_id] = False
        
        return checked_in_today
    
    def 
        
            
        
if __name__ == "__main__":
    table=StudentTable()
    checks = table.checkedin_today(1)
    
    
    #checkins=table.amount_Of_Checkins(1)
    #student_Attendance=table.calc_attendance(table.amount_Of_Checkins(1),table.calculate_Days(2))
    #names = table.get_Students_From_Checkin(1)
    #checks = table.amount_Of_Checkins(1)
    
    
    for x, y in checks.items():
        print(x, y)
    
    