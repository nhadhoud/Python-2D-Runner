import mysql.connector

class LeaderBoardDataBase():
    def __init__(self):
        super().__init__()
        try:
            self.mydb = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "root",
                database = "mydatabase"
            )
            mycursor = self.mydb.cursor()
            mycursor.execute("CREATE DATABASE IF NOT EXISTS mydatabase")
            mycursor.execute("""CREATE TABLE IF NOT EXISTS players (
                             playerName VARCHAR(255) PRIMARY KEY,
                             highScore INT)""")
        except:
            print("Could not initialise database")
        finally:
            if 'mycursor' in locals():
                mycursor.close()

    def update(self,name,score):
        try:
            mycursor = self.mydb.cursor()
            sql = "SELECT * FROM players WHERE playerName = %s"
            val = (name,)
            mycursor.execute(sql, val)
            result = mycursor.fetchone()

            if result:
                if score > result[1]:
                    sql = "UPDATE players SET highScore = %s WHERE playerName = %s"
                    val = (score, name)
                    mycursor.execute(sql, val)
                    self.mydb.commit()
            else:
                sql = "INSERT INTO players (playerName, highScore) VALUES (%s, %s)"
                val = (name, score)
                mycursor.execute(sql, val)
                self.mydb.commit()
        except:
            print("Error updating player data.")
        finally:
            if 'mycursor' in locals():
                mycursor.close()
        
    def getPlayer(self,name):
        try:
            mycursor = self.mydb.cursor()
            sql = "SELECT * FROM players WHERE playerName = %s"
            val = (name,)
            mycursor.execute(sql, val)
            result = mycursor.fetchone()
            return result
        except:
            print("Error fetching player data.")
            return None
        finally:
            if 'mycursor' in locals():
                mycursor.close()

    def getTopPlayers(self):
        try:
            mycursor = self.mydb.cursor()
            mycursor.execute("SELECT * FROM players ORDER BY highScore DESC LIMIT 5")
            result = mycursor.fetchall()
            return result
        except:
            print("Error fetching top players.")
            return []
        finally:
            if 'mycursor' in locals():
                mycursor.close()

    def getPlayerRank(self, name):
        try:
            mycursor = self.mydb.cursor()
            sql = "SELECT highScore FROM players WHERE playerName = %s"
            val = (name,)
            mycursor.execute(sql, val)
            playerHighScore = mycursor.fetchone()

            if playerHighScore:
                playerHighScore = playerHighScore[0]
                sql = "SELECT COUNT(*) FROM players WHERE highScore > %s"
                mycursor.execute(sql, (playerHighScore,))
                rank = mycursor.fetchone()[0] + 1
            else:
                rank = None

            return rank
        except:
            print("Error fetching player rank.")
            return None
        finally:
            if 'mycursor' in locals():
                mycursor.close()