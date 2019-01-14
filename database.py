import pymysql
import os

if os.name == 'nt':
    separator = '\\'
else:
    separator = '/'

database = pymysql.connect('localhost', 'root', 'anitscse034')
database.autocommit(True)
conn = database.cursor()
conn.execute('USE CodeDuel')

def get_contestant_name(c_id):
    query = "SELECT c_name FROM Contestant WHERE c_id = %s" % (c_id)
    conn.execute(query)
    contestant_name = conn.fetchone()[0]
    return contestant_name

def get_directory_path(d_id):
    query = "SELECT d_path FROM Directory WHERE d_id = '%s'" % (d_id)
    conn.execute(query)
    directory_path = conn.fetchone()[0]
    return directory_path

def get_contestant_dir(c_id):
    contestant_name = get_contestant_name(c_id)
    contestant_path = contestant_name.replace(' ', '')
    src_dir = get_directory_path('src')
    contestant_dir = src_dir + separator + contestant_path
    return contestant_dir

def get_test_filenames(p_id):
    query = "SELECT t_id, t_inputfile, t_outputfile FROM Testcase WHERE p_id = %s" % (p_id)
    conn.execute(query)
    test_filenames = conn.fetchall()
    return test_filenames

def get_score(c_id):
    query = "SELECT sum(points) FROM Score WHERE c_id = %s" % (c_id)
    conn.execute(query)
    score = conn.fetchone()[0]
    return score

def update_score(c_id, t_id, points):
    existence_test_query = "SELECT * FROM Score WHERE c_id = %s AND t_id = %s" % (c_id, t_id)
    conn.execute(existence_test_query)
    existence_test = len(conn.fetchall())

    if existence_test > 1:
        query = "UPDATE Score SET points = %s WHERE c_id = %s AND t_id = %s" % (points, c_id, t_id)
    else:
        query = "INSERT INTO Score VALUES (%s, %s, %s)" % (c_id, t_id, points)
    conn.execute(query)

def make_leaderboard():
    query = ''' SELECT C.c_name, (  SELECT sum(S.points)
                                    FROM Score S
                                    WHERE C.c_id = S.c_id   ) AS Total
                FROM Contestant C
                ORDER BY Total DESC'''
    conn.execute(query)
    leaderboard = conn.fetchall()
    return leaderboard

def get_opponent_id(c_id):
    query = "SELECT c_id_B FROM Duel WHERE c_id_A = %s" % (c_id)
    tuples_count = conn.execute(query)

    if tuples_count == 1:
        opponent_id = conn.fetchone()[0]
        return opponent_id

    query = "SELECT c_id_A FROM Duel WHERE c_id_B = %s" % (c_id)
    conn.execute(query)
    opponent_id = conn.fetchone()[0]
    return opponent_id