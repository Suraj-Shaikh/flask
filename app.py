from flask import Flask, jsonify, request  # Import request here
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains

# Database connection details
DB_HOST = "localhost"
DB_NAME = "pocra_gis"
DB_USER = "postgres"
DB_PASSWORD = "pocrapostgres"

# Connect to the PostgreSQL database
def get_db_connection():
    connection = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        options='-c client_encoding=UTF8'  # Enforce UTF-8 encoding
    )
    return connection

@app.route('/get_all_districts/<string:dtncode>', methods=['GET'])
def get_all_districts(dtncode):
    # Establish database connection
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)  # Use RealDictCursor to get results as dictionaries
    
    # Define the SQL query to get unique district names
    query = """
         SELECT dtncode, dtname,dtmname,is_pocra,
         CONCAT(
             ST_XMin(ST_Extent(geom)), ', ',
             ST_YMin(ST_Extent(geom)), ', ',
             ST_XMax(ST_Extent(geom)), ', ',
             ST_YMax(ST_Extent(geom))
            ) AS extent 
        FROM admin_layer.mh_district
        WHERE dtncode = %s
        GROUP BY dtncode, dtname,dtmname,is_pocra
        ORDER BY dtname
    """
    
    # Execute the query
    cur.execute(query,(dtncode,))
    result = cur.fetchall()
    
    # Close the database connection
    cur.close()
    conn.close()
    
    # Return the result as JSON
    return jsonify(result)


@app.route('/get_all_districts', methods=['GET'])
def get_districts():
    # Establish database connection
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)  # Use RealDictCursor to get results as dictionaries
    
    # Define the SQL query to get unique district names
    query = """
         SELECT dtncode, dtname,dtmname,is_pocra,
         CONCAT(
             ST_XMin(ST_Extent(geom)), ', ',
             ST_YMin(ST_Extent(geom)), ', ',
             ST_XMax(ST_Extent(geom)), ', ',
             ST_YMax(ST_Extent(geom))
            ) AS extent 
        FROM admin_layer.mh_district
        GROUP BY dtncode, dtname,dtmname,is_pocra
        ORDER BY dtname
    """
    
    # Execute the query
    cur.execute(query)
    result = cur.fetchall()
    
    # Close the database connection
    cur.close()
    conn.close()
    
    # Return the result as JSON
    return jsonify(result)

# taluka api for dropdown list
@app.route('/get_talukas/<string:dtncode>', methods=['GET'])
def get_talukas(dtncode):
    # Establish database connection
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)  # Use RealDictCursor to get results as dictionaries
    
    # Define the SQL query to get unique taluka names and codes for the specified district
    query = """
        SELECT dtname,dtncode, thname, thncode,thmname,
        CONCAT(
             ST_XMin(ST_Extent(geom)), ', ',
             ST_YMin(ST_Extent(geom)), ', ',
             ST_XMax(ST_Extent(geom)), ', ',
             ST_YMax(ST_Extent(geom))
            ) AS extent 
        FROM admin_layer.mh_village
        WHERE dtncode = %s
        GROUP BY dtname,dtncode, thname, thncode,thmname
        ORDER BY thname
    """
    
    # Execute the query with the provided district name
    cur.execute(query, (dtncode,))
    result = cur.fetchall()
    
    # Close the database connection
    cur.close()
    conn.close()
    
    # Return the result as JSON
    return jsonify(result)

# taluka api for Extent 
@app.route('/get_talukas/<string:dtncode>/<string:thncode>', methods=['GET'])
def get_talukas_ext(dtncode,thncode):
    # Establish database connection
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)  # Use RealDictCursor to get results as dictionaries
    
    # Define the SQL query to get unique taluka names and codes for the specified district
    query = """
        SELECT dtname,dtncode, thname, thncode,thmname,
        CONCAT(
             ST_XMin(ST_Extent(geom)), ', ',
             ST_YMin(ST_Extent(geom)), ', ',
             ST_XMax(ST_Extent(geom)), ', ',
             ST_YMax(ST_Extent(geom))
            ) AS extent 
        FROM admin_layer.mh_village
        WHERE dtncode = %s AND thncode = %s
        GROUP BY dtname,dtncode, thname, thncode,thmname
        ORDER BY thname
    """
    
    # Execute the query with the provided district name
    cur.execute(query, (dtncode,thncode))
    result = cur.fetchall()
    
    # Close the database connection
    cur.close()
    conn.close()
    
    # Return the result as JSON
    return jsonify(result)

# Village api for dropdown list
@app.route('/get_villages/<string:dtncode>/<string:thncode>', methods=['GET'])
def get_villages(dtncode, thncode):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    query = """
        SELECT DISTINCT dtname, dtncode, thname, thncode, vlname,vilmname, vincode, 
        CONCAT(
             ST_XMin(ST_Extent(geom)), ', ',
             ST_YMin(ST_Extent(geom)), ', ',
             ST_XMax(ST_Extent(geom)), ', ',
             ST_YMax(ST_Extent(geom))
            ) AS extent
        FROM admin_layer.mh_village
        WHERE dtncode = %s AND thncode = %s
        GROUP BY dtname, dtncode, thname, thncode, vlname,vilmname, vincode
        ORDER BY vlname
    """
    
    cur.execute(query, (dtncode, thncode))
    result = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return jsonify(result)

# Village api for Extent
@app.route('/get_villages/<string:dtncode>/<string:thncode>/<string:vincode>', methods=['GET'])
def get_villages_ext(dtncode, thncode,vincode):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    query = """
        SELECT DISTINCT dtname, dtncode, thname, thncode, vlname, vincode, 
        CONCAT(
             ST_XMin(ST_Extent(geom)), ', ',
             ST_YMin(ST_Extent(geom)), ', ',
             ST_XMax(ST_Extent(geom)), ', ',
             ST_YMax(ST_Extent(geom))
            ) AS extent
        FROM admin_layer.mh_village
        WHERE dtncode = %s AND thncode = %s AND vincode = %s
        GROUP BY dtname, dtncode, thname, thncode, vlname, vincode
        ORDER BY vlname
    """
    
    cur.execute(query, (dtncode, thncode,vincode))
    result = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return jsonify(result)

# Create NBSS Data api
@app.route('/get_soil_data', methods=['GET'])
def get_soil_data():
    # Get query parameters for district, taluka, and village codes   
    dtncode = request.args.get('dtncode', default=None, type=int)
    thncode = request.args.get('thncode', default=None, type=int)
    vincode = request.args.get('vincode', default=None, type=int)


    # Establish database connection
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)  # Use RealDictCursor to get results as dictionaries

    # Define the SQL query with optional filters
    query = """
        SELECT id, dtncode, thncode, vincode, dtname, thname, vlname, mini_water, gp_code, gp_name, phase_ii,
               vil_area, depth_class, texture_class, soc_class, ph_class, p_class, n_class, k_class, cec_class,
               bd_class, awc_class, depth_id, texture_id, soc_id, ph_id, p_id, n_id, k_id, cec_id, bd_id, awc_id,
               depth_remark, texture_remark, soc_remark, ph_remark, p_remark, n_remark, k_remark, cec_remark,
               bd_remark, awc_remark, depth_mclass, texture_mclass, soc_mclass, ph_mclass, p_mclass, n_mclass,
               k_mclass, cec_mclass, bd_mclass, awc_mclass,awc_mclass, soc_color, sd_color,texture_color,awc_color
        FROM nbss.nbss_all_soil_data
         WHERE (%s IS NULL OR dtncode = %s)
           AND (%s IS NULL OR thncode = %s)
           AND (%s IS NULL OR vincode = %s)
    """

    # Execute the query with parameters, passing each twice due to SQL positional formatting
    cur.execute(query, (dtncode, dtncode, thncode, thncode, vincode, vincode))
    result = cur.fetchall()

    # Close the database connection
    cur.close()
    conn.close()

    # Return the result as JSON
    return jsonify(result)


# Create API for District other soil parameters 
@app.route('/get_dist_other_soil_parameters', methods=['GET'])
def get_dist_other_soil_parameters():
    # Get query parameters for district, taluka, and village codes   
    dtncode = request.args.get('dtncode', default=None, type=int)
    phase = request.args.get('phase', default=None, type=int)


    # Establish database connection
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)  # Use RealDictCursor to get results as dictionaries

    # Define the SQL query with optional filters
    query = """
        SELECT dtncode, dtname, 
                MIN(min_n) as min_n, MAX(max_n) as max_n, 
                MIN(min_p) as min_p, MAX(max_p) as max_p, 
                MIN(min_k)as min_k, MAX(max_k) as max_k, 
                MIN(min_ph)as min_ph, MAX(max_ph) as max_ph,
                MIN(min_ec)as min_ec, MAX(max_ec) as max_ec, 
                MIN(min_bd)as min_bd, MAX(max_bd) as max_bd
        FROM nbss.village_soil_para_max_min
         WHERE (%s IS NULL OR dtncode = %s)
           AND (%s IS NULL OR phase = %s)
           GROUP BY dtncode, dtname
    """

    # Execute the query with parameters, passing each twice due to SQL positional formatting
    cur.execute(query, (dtncode, dtncode,phase,phase))
    result = cur.fetchall() 

    # Close the database connection
    cur.close()
    conn.close()

    # Return the result as JSON
    return jsonify(result)

# Create API for Taluka other soil parameters 
@app.route('/get_tal_other_soil_parameters', methods=['GET'])
def get_tal_other_soil_parameters():
    # Get query parameters for district, taluka, and village codes   
    dtncode = request.args.get('dtncode', default=None, type=int)
    thncode = request.args.get('thncode', default=None, type=int)
    phase = request.args.get('phase', default=None, type=int)


    # Establish database connection
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)  # Use RealDictCursor to get results as dictionaries

    # Define the SQL query with optional filters
    query = """
        SELECT dtncode, dtname, thncode, thname,
                MIN(min_n) as min_n, MAX(max_n) as max_n, 
                MIN(min_p) as min_p, MAX(max_p) as max_p, 
                MIN(min_k)as min_k, MAX(max_k) as max_k, 
                MIN(min_ph)as min_ph, MAX(max_ph) as max_ph,
                MIN(min_ec)as min_ec, MAX(max_ec) as max_ec, 
                MIN(min_bd)as min_bd, MAX(max_bd) as max_bd
        FROM nbss.village_soil_para_max_min
         WHERE (%s IS NULL OR dtncode = %s)
              AND (%s IS NULL OR thncode = %s)
              AND (%s IS NULL OR phase = %s)
              GROUP BY dtncode, dtname, thncode, thname
    """

    # Execute the query with parameters, passing each twice due to SQL positional formatting
    cur.execute(query, (dtncode, dtncode, thncode, thncode, phase,phase))
    result = cur.fetchall() 

    # Close the database connection
    cur.close()
    conn.close()

    # Return the result as JSON
    return jsonify(result)

# Create API for Village other soil parameters 
@app.route('/get_vill_other_soil_parameters', methods=['GET'])
def get_vill_other_soil_parameters():
    # Get query parameters for district, taluka, and village codes   
    dtncode = request.args.get('dtncode', default=None, type=int)
    thncode = request.args.get('thncode', default=None, type=int)
    vincode = request.args.get('vincode', default=None, type=int)
    phase = request.args.get('phase', default=None, type=int)


    # Establish database connection
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)  # Use RealDictCursor to get results as dictionaries

    # Define the SQL query with optional filters
    query = """
        SELECT dtncode, dtname, thncode, thname,vincode, vlname, 
                MIN(min_n) as min_n, MAX(max_n) as max_n, 
                MIN(min_p) as min_p, MAX(max_p) as max_p, 
                MIN(min_k)as min_k, MAX(max_k) as max_k, 
                MIN(min_ph)as min_ph, MAX(max_ph) as max_ph,
                MIN(min_ec)as min_ec, MAX(max_ec) as max_ec, 
                MIN(min_bd)as min_bd, MAX(max_bd) as max_bd
        FROM nbss.village_soil_para_max_min
         WHERE (%s IS NULL OR dtncode = %s)
              AND (%s IS NULL OR thncode = %s)
              AND (%s IS NULL OR vincode = %s)
              AND (%s IS NULL OR phase = %s)
              GROUP BY dtncode, dtname, thncode, thname,vincode, vlname
    """

    # Execute the query with parameters, passing each twice due to SQL positional formatting
    cur.execute(query, (dtncode, dtncode, thncode, thncode,vincode, vincode, phase,phase))
    result = cur.fetchall() 

    # Close the database connection
    cur.close()
    conn.close()

    # Return the result as JSON
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
