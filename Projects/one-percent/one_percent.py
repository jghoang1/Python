import sqlite3
import sys
import os
import datetime
import math
import re
import matplotlib.pyplot as plt
import pandas as pd

class DBManager:

    DB_FN = "running_data.db"
    LAP_LENGTH = 0.25 # miles

    def __init__(self):
        self.parent_dir = os.path.dirname(os.path.abspath(__file__))
        self.path_to_db = os.path.join(self.parent_dir, self.DB_FN)
        self.con = sqlite3.connect(self.path_to_db)
        self.cur = self.con.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS run_data(
                        laps, 
                        times, 
                        average_pace, 
                        fastest_lap, 
                        date)""")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS best_data(
                         most_laps, 
                         most_laps_date, 
                         best_average_pace, 
                         best_average_pace_date, 
                         fastest_lap, 
                         fastest_lap_date)""")

    def get_best_stats(self):
        res = self.cur.execute("SELECT * from best_data").fetchone()
        if res is None:
            res = (None, None, None, None, None, None)
        return res 
    
    def insert_data(self, laps, times, date=datetime.date.today()):
        """
        Inserts new data into run_data table. Calls get_best_stats 
        and updates best_data if necessary

        Args:
            laps (int, float): laps ran
            times (list): list of lap times, in seconds
            date (datetime.date, optional): date of entry. Defaults to datetime.date.today().
        """
        assert len(times) == math.ceil(laps) 
        entry_average_pace = sum(times)/laps * 1/self.LAP_LENGTH  # seconds / mile

        entry_fastest_lap = min(times[:int(laps)-1])
        most_laps, most_laps_date, best_average_pace, best_average_pace_date, fastest_lap, fastest_lap_date = self.get_best_stats()

        

        # compare with best stats
        print("Run Overview for {}:".format(date))
        print("="*40)

        print("Laps ran: \t\t\t\t {:.2f} laps ({:.2f} miles)".format(laps, laps*self.LAP_LENGTH))

        if most_laps is None:
            most_laps = laps
            most_laps_date = date
        elif laps > most_laps:
            print("\tMost laps ran: \t {}: \t {:.2f} laps ({:.2f} miles)".format(most_laps_date, most_laps, most_laps*self.LAP_LENGTH))
            print("\tYou beat your previous distance by {:.2f}%".format(100 * (laps-most_laps)/most_laps))
            print("\tCongrats!")
            most_laps = laps
            most_laps_date = date
            print("\tGoal: {:.2f} laps ({:.2f} miles)".format(most_laps * 1.01, most_laps*1.01*self.LAP_LENGTH))
        else:
            print("\tMost laps ran: \t{}: \t {:.2f} laps ({:.2f} miles)".format(most_laps_date, most_laps, most_laps*self.LAP_LENGTH))

    
        print("\nAvg pace: \t\t\t\t {} per mile".format(self._s_to_min(entry_average_pace)))
        if best_average_pace is None:
            best_average_pace = entry_average_pace
            best_average_pace_date = date
        elif entry_average_pace < best_average_pace:
            print("\tFastest pace: \t {}: \t {} per mile".format(best_average_pace_date, self._s_to_min(best_average_pace)))
            print("\tYou beat your previous pace by {:.2f}%".format(100 * (best_average_pace-entry_average_pace)/best_average_pace))
            print("\tCongrats!")
            best_average_pace = entry_average_pace
            best_average_pace_date = date
            print("\tGoal: {:} per mile".format(self._s_to_min(best_average_pace * 0.99)))
        else:
            print("\tFastest pace: \t {}: \t {} per mile".format(best_average_pace_date, self._s_to_min(best_average_pace)))

        print("\nFastest lap: \t\t\t\t {}".format(self._s_to_min(entry_fastest_lap)))
        if fastest_lap is None:
            fastest_lap = entry_fastest_lap
            fastest_lap_date = date
        elif entry_fastest_lap < fastest_lap:
            print("\tRecord lap: \t {}: \t {}".format(fastest_lap_date, self._s_to_min(fastest_lap)))
            print("\tBeat previous fastest lap by {:.2f}%".format(100 * (fastest_lap-entry_fastest_lap)/fastest_lap))
            print("\tCongrats!")
            fastest_lap = entry_fastest_lap
            fastest_lap_date = date
            print("\tGoal: {}".format(self._s_to_min(fastest_lap*0.99)))
        else:
            print("\tRecord lap: \t {}: \t {}".format(fastest_lap_date, self._s_to_min(fastest_lap)))
        
        # insert into run_data
        self.cur.execute("""
                        INSERT INTO run_data VALUES
                            (?,?,?,?,?)
                        """, (laps, str(times), entry_average_pace, entry_fastest_lap, date))
        self.con.commit()


        # Delete existing stats and replace with new bests
        self.cur.execute("""DELETE FROM best_data""")
        self.cur.execute("""
                        INSERT INTO best_data VALUES
                            (?,?,?,?,?,?)
                        """, (most_laps, most_laps_date, best_average_pace, best_average_pace_date, fastest_lap, fastest_lap_date))
        self.con.commit()

    def display_best_stats(self):
        """
        Print best stats to console
        """
        most_laps, most_laps_date, best_average_pace, best_average_pace_date, fastest_lap, fastest_lap_date = self.get_best_stats()
        print("Current records:")
        print("="*40)
        print("Most laps ran: \t {}: \t {:.2f} laps ({:.2f} miles)".format(most_laps_date, most_laps, most_laps*self.LAP_LENGTH))
        print("\tGoal: {:.2f} laps ({:.2f} miles)".format(most_laps * 1.01, most_laps*1.01*self.LAP_LENGTH))
        print("Fastest pace: \t {}: \t {} per mile".format(best_average_pace_date, self._s_to_min(best_average_pace)))
        print("\tGoal: {:} per mile".format(self._s_to_min(best_average_pace * 0.99)))
        print("Record lap: \t {}: \t {}".format(fastest_lap_date, self._s_to_min(fastest_lap)))
        print("\tGoal: {}".format(self._s_to_min(fastest_lap*0.99)))

    def get_n_latest_runs(self, n):
        res = self.cur.execute("SELECT * from run_data ORDER BY date DESC LIMIT {}".format(n))
        return res.fetchall()
    
    def _clear_runs(self):
        """
        For debugging
        """
        self.cur.execute("""DELETE FROM run_data""")
        self.con.commit()

    def _s_to_min(self, s):
        """
        Convert seconds to str

        Args:
            s (int): seconds
        """
        s = int(s)
        if s > 3600:
            return "{}:{:0>2}:{:0>2}:".format(s//3600, (s%3600)//60, (s%3600)%60)
        else:
            return "{}:{:0>2}".format(s//60, s%60)

    def _str_to_s(self, time):
        """
        Convert time string in mm:ss format to seconds

        Args:
            time (str): time "mm:ss"
        """
        try:
            m,s = re.split(':|\.', time)
            m = int(m)
            s = int(s)
        except:
            raise ValueError("Invalid time given: {}. (should be in 'mm:ss' format.)".format(time))
        assert s < 60, "Seconds must be less than 60. Got {}".format(time)

        return 60 * m + s

    def graph_all_runs(self):
        pass
        res = self.cur.execute("""
                                select *  
                                from run_data
                                where date > date('now','-90 days'); 
                                """)
        points = res.fetchall()

        most_laps, most_laps_date, best_average_pace, best_average_pace_date, fastest_lap, fastest_lap_date = self.get_best_stats()
        plt.figure(figsize=(16, 4))

        df = pd.DataFrame(points)

        # Laps
        plt.subplot(1, 3, 1)
        plt.plot(df.loc[:, 4], df.loc[:, 0], linewidth=3)
        plt.plot(most_laps_date, most_laps, "or")
        plt.axhline(y=most_laps*1.01, color='r', linestyle='--', label="{}".format(most_laps*1.01))
        plt.legend()
        plt.title('Laps', fontsize = 12)
        plt.grid()

        # Pace
        ax = plt.subplot(1, 3, 2)
        plt.plot(df.loc[:, 4], df.loc[:, 2], linewidth=3)
        plt.plot(best_average_pace_date, best_average_pace, "or")
        plt.axhline(y=best_average_pace*0.99, color='r', linestyle='--', label="{}".format(self._s_to_min(best_average_pace*0.99)))
        plt.legend()
        plt.title('Avg Pace', fontsize = 12)
        ax.yaxis.set_major_formatter(lambda x,pos: self._s_to_min(x))
        ax.yaxis.set
        plt.grid()

        # Fastest lap
        ax = plt.subplot(1, 3, 3)
        plt.plot(df.loc[:, 4], df.loc[:, 3], linewidth=3)
        plt.plot(fastest_lap_date, fastest_lap, "or")
        plt.axhline(y=fastest_lap*0.99, color='r', linestyle='--', label="{}".format(self._s_to_min(fastest_lap*0.99)))
        plt.title('Fastest Lap', fontsize = 12)
        plt.legend()
        ax.yaxis.set_major_formatter(lambda x,pos: self._s_to_min(x))
        plt.grid()
        
        plt.show()



if __name__== "__main__":
    """
    Format:
    python one-percent.py laps_ran lap1_time lat2_time ... -d YYYY-MM-DD

    """
    args = sys.argv[1:]
    manager = DBManager()
    # if no additional args given, show current best stats
    if len(args) == 0:
        manager.display_best_stats()
        manager.graph_all_runs()

    else:
        date = datetime.date.today()
        parsed_args = args[:]
        for i in range(len(args)):
            if args[i] == "-d":
                date = args[i+1]
                try:
                    date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
                except:
                    raise ValueError("Date must be in 'YYYY-MM-DD' format")
                parsed_args.pop(i)
                parsed_args.pop(i)
                
        args = parsed_args
        laps = float(args[0])
        times = [manager._str_to_s(time) for time in args[1:]]

        manager.insert_data(laps, times, date)
        manager.graph_all_runs()