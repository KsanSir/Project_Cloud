from flask import Flask, flash, jsonify, render_template, request, redirect, url_for, session
from mysql import connector
from datetime import datetime
import mysql.connector

app = Flask(__name__)
app.secret_key = 'many random bytes'

# Function to create a new database connection
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='',  # Use an empty password as per your specification
        database='laundry_on'
    )

@app.route('/')
def home():
    if not session.get('logged_in'):
        return redirect('/login/')
    else:
        return redirect('/dashboard_kasir/')
    
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        
        db = get_db_connection()
        cursor = db.cursor()
        
        try:
            cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
            account = cursor.fetchone()
            
            if account:
                session['username'] = account[1]  # Assuming the username is in the second column
                session['loggedin'] = True
                return redirect('/dashboard_kasir/')
            else:
                flash("Username / password salah!")
        finally:
            cursor.close()
            db.close()

    return render_template('login.html', error=None)

@app.route('/dashboard_kasir/')
def dash_kasir():
    db = get_db_connection()
    cursor = db.cursor()
    
    try:
        cursor.execute("SELECT COUNT(id_pelanggan) FROM pelanggan;")
        jml_pelanggan = str(cursor.fetchall()[0][0])
        
        cursor.execute("SELECT COUNT(id_nota) FROM transaksi;")
        jml_pesanan = str(cursor.fetchall()[0][0])
        
        cursor.execute("SELECT COUNT(id_nota) FROM transaksi WHERE status = 'PROSES' OR status = 'DITERIMA';")
        belum_selesai = str(cursor.fetchall()[0][0])
        
    finally:
        cursor.close()
        db.close()

    return render_template('kasir/dash_kasir.html', jml_pelanggan=jml_pelanggan, jml_pesanan=jml_pesanan, belum_selesai=belum_selesai)

@app.route('/jumlahPelanggan/')
def jumlah_pelanggan():
    db = get_db_connection()
    cursor = db.cursor()
    
    try:
        cursor.execute("SELECT COUNT(id_pelanggan) FROM pelanggan;")
        jml_pelanggan = str(cursor.fetchall()[0][0])
    finally:
        cursor.close()
        db.close()

    return redirect('/base_kasir/', jml_pelanggan)

@app.route('/tambah_pesanan/')
def tambah_pesanan():
    return render_template('kasir/tambah_pesanan.html')

@app.route('/pelanggan/')
def pelanggan():
    q = request.args.get('q', '')
    db = get_db_connection()
    cursor = db.cursor()
    
    try:
        cursor.execute("SELECT id_pelanggan, nama FROM pelanggan WHERE nama LIKE %s", ("%{}%".format(q),))
        result = cursor.fetchall()
    finally:
        cursor.close()
        db.close()

    pelanggan = [{'id': user[0], 'text': user[1]} for user in result]
    return jsonify(pelanggan)

@app.route('/karyawan/')
def karyawan():
    q = request.args.get('q', '')
    
    # Get a database connection
    db = get_db_connection()
    
    try:
        with db.cursor() as cursor:
            cursor.execute(
                "SELECT id_karyawan, nama FROM karyawan WHERE nama LIKE %s", ("%{}%".format(q),)
            )
            result = cursor.fetchall()
        
        # Prepare the response
        karyawan = [{'id': user[0], 'text': user[1]} for user in result]
        return jsonify(karyawan)
    
    except Exception as e:
        # Handle any errors that occur during the database operation
        return jsonify({'error': str(e)}), 500
    
    finally:
        db.close()

# Route to display the transaction form
@app.route('/transaksi/', methods=['GET', 'POST'])
def transaksi():
    if request.method == 'POST':
        # Get form data
        id_pelanggan = request.form['id_pelanggan']
        jenis_laundry = request.form['jenis_laundry']
        berat = request.form['berat']
        tanggal_masuk = request.form['tanggal_masuk']
        nama_karyawan = request.form['nama_karyawan']
        status_pembayaran = request.form['status_pembayaran']
        status_pesanan = 'DITERIMA'
        suffix = jenis_laundry[0] + datetime.today().strftime('%d%m%y')

        # Establish database connection
        db = get_db_connection()
        if db is None:
            flash("Database connection failed.", 'danger')
            return redirect(url_for('transaksi'))  # Redirect to the transaction form

        cur = db.cursor()
        try:
            # Get the last nota number for the given suffix
            cur.execute('''
            SELECT 
                IFNULL(
                    LEFT(
                    MAX(id_nota),
                    3
                    ), 
                    0
                ) as last_nota 
            FROM 
                transaksi 
            WHERE 
                RIGHT(
                    id_nota, 
                    7
                ) = %s;
            ''', (suffix,))
            
            last_nota = cur.fetchone()[0]
            
            # Generate new nota ID
            new_order = "00" + str(int(last_nota) + 1)
            new_nota = new_order[-3:] + suffix
            
            # Insert the new transaction
            cur.execute('''
            INSERT INTO transaksi (id_nota, id_pelanggan, jenis_laundry, berat, tanggal_masuk, id_karyawan, status_pembayaran, status) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', (new_nota, id_pelanggan, jenis_laundry, berat, tanggal_masuk, nama_karyawan, status_pembayaran, status_pesanan))
            
            db.commit()
            flash("Transaksi berhasil ditambahkan", 'success')
        except Exception as e:
            db.rollback()  # Rollback if there is any error
            flash(f"Error: {str(e)}", 'danger')
        finally:
            cur.close()
            db.close()

        return redirect(url_for('nota_transaksi', id_nota=new_nota))

    return render_template('transaksi.html')

@app.route('/no_nota/')
def no_nota():
    suffix = datetime.today().strftime('%d%m%y')
    db = get_db_connection()
    cur = db.cursor()
    
    try:
        cur.execute('''
        SELECT 
            IFNULL(
                LEFT(
                MAX(id_nota),
                3
                ), 
                0
            ) as last_nota 
        FROM 
            transaksi 
        WHERE 
            RIGHT(
                id_nota, 
                7
            ) = %s;
        ''', [suffix,])
        last_nota = cur.fetchone()[0]

        new_order = "00" + str(int(last_nota) + 1)
        new_nota = new_order[-3:] + suffix
    finally:
        cur.close()
        db.close()

    return jsonify(new_nota)    
    

# Route Tambah Pelanggan
@app.route('/tambah_pelanggan/')
def tambah_pelanggan():
    return render_template('kasir/tambah_pelanggan.html')

@app.route('/proses_tambah/', methods=['POST'])
def proses_tambah_pelanggan():
    nama = request.form['nama']
    alamat = request.form['alamat']
    kontak = request.form['kontak']
    
    db = get_db_connection()
    cur = db.cursor()
    
    try:
        cur.execute('INSERT INTO pelanggan (nama, alamat, kontak) VALUES (%s, %s, %s)', (nama, alamat, kontak))
        db.commit()
        flash("Pelanggan berhasil ditambahkan!", 'success')
    except Exception as e:
        db.rollback()
        flash(f"Error: {str(e)}", 'danger')
    finally:
        cur.close()
        db.close()

    return redirect('/tambah_pelanggan/')

# Route Data Pelanggan
@app.route('/data_pelanggan/')
def data_pelanggan():
    db = get_db_connection()
    cursor = db.cursor()
    
    try:
        cursor.execute("SELECT LPAD(id_pelanggan, 4, '0') AS id_pelanggan_zerofill, nama, kontak, alamat FROM pelanggan")
        result = cursor.fetchall()
    finally:
        cursor.close()
        db.close()

    return render_template('kasir/data_pelanggan.html', dt_pelanggan=result)

# Route Ubah Data Pelanggan
@app.route('/ubah_pelanggan/<id_pelanggan>')
def ubah_data_pelanggan(id_pelanggan):
    db = get_db_connection()
    cur = db.cursor()
    
    try:
        cur.execute('SELECT * FROM pelanggan WHERE id_pelanggan=%s', (id_pelanggan,))
        res = cur.fetchall()
    finally:
        cur.close()
        db.close()

    return render_template('kasir/ubah_data_pelanggan.html', data=res)

# Route proses ubah
@app.route('/proses_ubah_pelanggan/', methods=['POST'])
def proses_ubah_pelanggan():
    id_pelanggan = request.form['id_pelanggan']
    nama = request.form['nama']
    kontak = request.form['kontak']
    alamat = request.form['alamat']
    
    db = get_db_connection()
    cur = db.cursor()
    
    try:
        sql = "UPDATE pelanggan SET nama=%s, kontak=%s, alamat=%s WHERE id_pelanggan=%s"
        value = (nama, kontak, alamat, id_pelanggan)
        cur.execute(sql, value)
        db.commit()
        flash("Data pelanggan berhasil diubah!", 'success')
    except Exception as e:
        db.rollback()
        flash(f"Error: {str(e)}", 'danger')
    finally:
        cur.close()
        db.close()

    return redirect(url_for('data_pelanggan'))

# Route untuk menghapus data pelanggan
@app.route('/hapus/<int:id_pelanggan>', methods=['GET'])
def hapus_data(id_pelanggan):
    db = get_db_connection()
    cur = db.cursor()
    
    try:
        # Delete data from the transaksi table that is related to id_pelanggan
        cur.execute('DELETE FROM transaksi WHERE id_pelanggan=%s', (id_pelanggan,))
        # Delete data from the pelanggan table
        cur.execute('DELETE FROM pelanggan WHERE id_pelanggan=%s', (id_pelanggan,))
        # Commit changes
        db.commit()
        flash('Data berhasil dihapus', 'success')
    except Exception as e:
        db.rollback()  # Rollback if there is any error
        flash(f"Error: {str(e)}", 'danger')
    finally:
        cur.close()
        db.close()

    return redirect(url_for('data_pelanggan'))

# Route Riwayat Pesanan
@app.route('/riwayat_pesanan/')
def riwayat_pesanan():
    db = get_db_connection()
    cursor = db.cursor()
    
    try:
        cursor.execute('''SELECT transaksi.id_nota, pelanggan.nama, transaksi.jenis_laundry,
                        transaksi.berat, transaksi.tanggal_masuk,
                        (transaksi.berat * jenis_paket.harga) AS total_harga, karyawan.nama
                        FROM transaksi
                        INNER JOIN pelanggan ON transaksi.id_pelanggan = pelanggan.id_pelanggan
                        INNER JOIN karyawan ON transaksi.id_karyawan = karyawan.id_karyawan
                        INNER JOIN jenis_paket ON transaksi.jenis_laundry = jenis_paket.jenis_laundry
                        ORDER BY transaksi.id_nota ASC;''')
        result = cursor.fetchall()
    finally:
        cursor.close()
        db.close()

    return render_template('kasir/riwayat_pesanan.html', transaksi=result)

# Route Status Pesanan
@app.route('/status_pesanan/')
def status_pesanan():
    db = get_db_connection()
    if db is None:
        flash("Database connection failed.", 'danger')
        return render_template('kasir/status_pesanan.html', status=[])

    cursor = db.cursor()
    try:
        cursor.execute('''
        SELECT 
            transaksi.id_nota, 
            pelanggan.nama, 
            transaksi.status, 
            transaksi.status_pembayaran, 
            transaksi.tanggal_keluar
        FROM 
            transaksi 
        INNER JOIN
            pelanggan ON transaksi.id_pelanggan = pelanggan.id_pelanggan;
        ''')
        result = cursor.fetchall()
    except Exception as e:
        flash(f"Error fetching status pesanan: {str(e)}", 'danger')
        result = []
    finally:
        cursor.close()
        db.close()
    
    return render_template('kasir/status_pesanan.html', status=result)

# Proses ubah status pesanan
@app.route('/proses_ubah_status/', methods=['POST'])
def proses_ubah_status():
    id_nota = request.form['id_nota']
    status = request.form['status_pesanan']
    status_pembayaran = request.form['status_pembayaran']
    tanggal_keluar = request.form['tanggal_keluar']
    
    db = get_db_connection()
    cur = db.cursor()
    
    try:
        sql = "UPDATE transaksi SET status=%s, status_pembayaran=%s, tanggal_keluar=%s WHERE id_nota=%s"
        value = (status, status_pembayaran, tanggal_keluar, id_nota)
        cur.execute(sql, value)
        db.commit()
        flash("Status pesanan berhasil diubah!", 'success')
    except Exception as e:
        db.rollback()
        flash(f"Error: {str(e)}", 'danger')
    finally:
        cur.close()
        db.close()

    return redirect(url_for('status_pesanan'))

# Route to display the nota
@app.route('/nota_transaksi/<id_nota>')
def nota_transaksi(id_nota):
    db = get_db_connection()
    cursor = db.cursor()
    
    try:
        cursor.execute("""
            SELECT 
                transaksi.id_nota,
                pelanggan.nama, 
                transaksi.jenis_laundry, 
                transaksi.berat, 
                transaksi.tanggal_masuk, 
                (transaksi.berat * jenis_paket.harga) AS total_harga, 
                transaksi.status_pembayaran
            FROM 
                transaksi
            INNER JOIN 
                pelanggan ON transaksi.id_pelanggan = pelanggan.id_pelanggan
            INNER JOIN 
                jenis_paket ON transaksi.jenis_laundry = jenis_paket.jenis_laundry
            WHERE 
                transaksi.id_nota = %s;
        """, (id_nota,))
        
        result = cursor.fetchone()
        
        if result is None:
            flash("Transaksi tidak ditemukan.", 'warning')
            return redirect(url_for('transaksi'))  # Redirect to the transaction form

    except Exception as e:
        flash(f"Terjadi kesalahan: {str(e)}", 'danger')
        return redirect(url_for('transaksi'))  # Redirect to the transaction form
    finally:
        cursor.close()
        db.close()

    return render_template('kasir/nota.html', hasil=result)

# Halaman Informasi Harga
@app.route('/informasi_harga/')
def info_harga():
    db = get_db_connection()
    cur = db.cursor()
    
    try:
        cur.execute("SELECT * FROM jenis_paket")
        res = cur.fetchall()
    finally:
        cur.close()
        db.close()

    return render_template('kasir/info_paket.html', paket=res)

# Dashboard Manajer
@app.route('/dashboard_manajer/')
def dash_manajer():
    db = get_db_connection()
    cursor = db.cursor()
    
    try:
        cursor.execute("SELECT COUNT(id_nota) FROM transaksi")
        result = cursor.fetchall()[0][0]
        cursor.execute("SELECT COUNT(id_pelanggan) FROM pelanggan")
        jml_pelanggan = cursor.fetchall()[0][0]
        cursor.execute("SELECT COUNT(id_karyawan) FROM karyawan")
        jml_karyawan = cursor.fetchall()[0][0]
    finally:
        cursor.close()
        db.close()

    return render_template('manajer/dash_manajer.html', jml_pesanan=result, jml_pelanggan=jml_pelanggan, jml_karyawan=jml_karyawan)

# Route data karyawan
@app.route('/data_karyawan/')
def data_karyawan():
    db = get_db_connection()
    cursor = db.cursor()
    
    try:
        cursor.execute('''SELECT karyawan.id_karyawan, karyawan.kode_karyawan, karyawan.nama, 
                        karyawan.kontak, karyawan.alamat, karyawan.jam_kerja,
                        (karyawan.jam_kerja * posisi.gaji_pokok) AS gaji
                        FROM karyawan
                        INNER JOIN posisi ON karyawan.kode_karyawan = posisi.kode_karyawan''')
        result = cursor.fetchall()
    finally:
        cursor.close()
        db.close()

    return render_template('manajer/data_karyawan.html', dt_karyawan=result)

# Gaji Pokok
@app.route('/gaji_pokok/')
def gaji_pokok():
    db = get_db_connection()
    cursor = db.cursor()
    
    try:
        cursor.execute("SELECT * FROM posisi;")
        result = cursor.fetchall()
    finally:
        cursor.close()
        db.close()

    return render_template('manajer/gaji_pokok.html', gaji=result)

@app.route('/tambah_posisi/', methods=['POST'])
def tambah_posisi():
    flash("Data Inserted Successfully")
    kode_karyawan = request.form['kode_karyawan']
    jobdesk = request.form['jobdesk']
    gaji_pokok = request.form['gaji_pokok']
    
    db = get_db_connection()
    cur = db.cursor()
    
    try:
        cur.execute('INSERT INTO posisi (kode_karyawan, jobdesk, gaji_pokok) VALUES (%s, %s, %s)', 
                    (kode_karyawan, jobdesk, gaji_pokok))
        db.commit()
    except Exception as e:
        db.rollback()
        flash(f"Error: {str(e)}", 'danger')
    finally:
        cur.close()
        db.close()

    return redirect(url_for('gaji_pokok'))

@app.route('/update_gaji/', methods=['GET', 'POST'])
def update_gaji():
    kode_karyawan = request.form['kode_karyawan']
    posisi = request.form['jobdesk']
    gaji_pokok = request.form['gaji_pokok']
    
    db = get_db_connection()
    cursor = db.cursor()
    
    try:
        sql = '''
            UPDATE posisi
            SET kode_karyawan = %s,
                jobdesk = %s,
                gaji_pokok = %s
            WHERE kode_karyawan = %s
        '''
        value = (kode_karyawan, posisi, gaji_pokok, kode_karyawan)
        cursor.execute(sql, value)
        db.commit()
        flash("Data Updated Successfully")
    except Exception as e:
        db.rollback()
        flash(f"Error: {str(e)}", 'danger')
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('gaji_pokok'))

@app.route('/hapus_gaji/<kode_karyawan>', methods=['GET'])
def hapus_gaji(kode_karyawan):
    flash("Record Has Been Deleted Successfully")
    
    db = get_db_connection()
    cur = db.cursor()
    
    try:
        cur.execute("DELETE FROM posisi WHERE kode_karyawan=%s", (kode_karyawan,))
        db.commit()
    except Exception as e:
        db.rollback()
        flash(f"Error: {str(e)}", 'danger')
    finally:
        cur.close()
        db.close()

    return redirect(url_for('gaji_pokok'))

# Route Riwayat Pesanan
@app.route('/M.riwayat_pesan/')
def data_Mriwayat_pesanan():
    db = get_db_connection()
    cursor = db.cursor()
    
    try:
        cursor.execute('''
            SELECT transaksi.id_nota, pelanggan.nama, transaksi.jenis_laundry,
                   transaksi.berat, transaksi.tanggal_keluar,
                   (transaksi.berat * jenis_paket.harga) AS total_harga, 
                   karyawan.nama, transaksi.status
            FROM transaksi
            INNER JOIN pelanggan ON transaksi.id_pelanggan = pelanggan.id_pelanggan
            INNER JOIN karyawan ON transaksi.id_karyawan = karyawan.id_karyawan
            INNER JOIN jenis_paket ON transaksi.jenis_laundry = jenis_paket.jenis_laundry
            ORDER BY transaksi.id_nota ASC;
        ''')
        result = cursor.fetchall()
    finally:
        cursor.close()
        db.close()

    return render_template('manajer/M.riwayat_pesan.html', transaksi=result)

# Route data pelanggan
@app.route('/M.data_pelanggan/')
def Mdata_pelanggan():
    db = get_db_connection()
    cursor = db.cursor()
    
    try:
        cursor.execute("SELECT LPAD(id_pelanggan, 4, '0') AS id_pelanggan_zerofill, nama, kontak, alamat FROM pelanggan")
        result = cursor.fetchall()
    finally:
        cursor.close()
        db.close()

    return render_template('manajer/M.data_pelanggan.html', dt_pelanggan=result)


@app.route('/tambah_karyawan/', methods=['POST'])
def tambah_karyawan():
    flash("Data Inserted Successfully")
    id_karyawan = request.form['id_karyawan']
    kode_karyawan = request.form['kode_karyawan']
    nama = request.form['nama']
    kontak = request.form['kontak']
    alamat = request.form['alamat']
    jam_kerja = request.form['jam_kerja']
    
    db = get_db_connection()
    cur = db.cursor()
    
    try:
        cur.execute('INSERT INTO karyawan (id_karyawan, kode_karyawan, nama, kontak, alamat, jam_kerja) VALUES (%s, %s, %s, %s, %s, %s)', 
                    (id_karyawan, kode_karyawan, nama, kontak, alamat, jam_kerja))
        db.commit()
    except Exception as e:
        db.rollback()
        flash(f"Error: {str(e)}", 'danger')
    finally:
        cur.close()
        db.close()

    return redirect(url_for('data_karyawan'))

@app.route('/hapus_karyawan/<id_karyawan>', methods=['GET'])
def hapus_karyawan(id_karyawan):
    flash("Record Has Been Deleted Successfully")
    
    db = get_db_connection()
    cur = db.cursor()
    
    try:
        cur.execute("DELETE FROM karyawan WHERE id_karyawan=%s", (id_karyawan,))
        db.commit()
    except Exception as e:
        db.rollback()
        flash(f"Error: {str(e)}", 'danger')
    finally:
        cur.close()
        db.close()

    return redirect(url_for('data_karyawan'))

@app.route('/update_karyawan/', methods=['GET', 'POST'])
def update_karyawan():
    id_karyawan = request.form['id_karyawan']
    kode_karyawan = request.form['kode_karyawan']
    nama = request.form['nama']
    kontak = request.form['kontak']
    alamat = request.form['alamat']
    jam_kerja = request.form['jam_kerja']
    
    db = get_db_connection()
    cursor = db.cursor()
    
    try:
        sql = '''UPDATE karyawan 
                 SET kode_karyawan=%s, 
                     nama=%s, 
                     kontak=%s, 
                     alamat=%s, 
                     jam_kerja=%s
                 WHERE id_karyawan=%s;'''
        value = (kode_karyawan, nama, kontak, alamat, jam_kerja, id_karyawan)
        cursor.execute(sql, value)
        db.commit()
        flash("Data Updated Successfully")
    except Exception as e:
        db.rollback()
        flash(f"Error: {str(e)}", 'danger')
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('data_karyawan'))

# Route Data Paket
@app.route('/kelola_paket/')
def kelola_paket():
    db = get_db_connection()
    cursor = db.cursor()
    
    try:
        cursor.execute("SELECT * FROM jenis_paket")
        result = cursor.fetchall()
    finally:
        cursor.close()
        db.close()

    return render_template('manajer/kelola_paket.html', paket=result)

@app.route('/update_paket/', methods=['GET', 'POST'])
def update_paket():
    nama_paket = request.form['nama_paket']
    harga = request.form['harga']
    
    db = get_db_connection()
    cur = db.cursor()
    
    try:
        sql = '''UPDATE jenis_paket
                 SET harga=%s
                 WHERE jenis_laundry=%s'''
        value = (harga, nama_paket)
        cur.execute(sql, value)
        db.commit()
        flash("Data Updated Successfully")
    except Exception as e:
        db.rollback()
        flash(f"Error: {str(e)}", 'danger')
    finally:
        cur.close()
        db.close()

    return redirect(url_for('kelola_paket'))

@app.route('/tambah_paket/', methods=['POST'])
def tambah_paket():
    flash("Data Inserted Successfully")
    nama_paket = request.form['nama_paket']
    harga = request.form['harga']
    
    db = get_db_connection()
    cur = db.cursor()
    
    try:
        cur.execute('INSERT INTO jenis_paket (jenis_laundry, harga) VALUES (%s, %s)', 
                    (nama_paket, harga))
        db.commit()
    except Exception as e:
        db.rollback()
        flash(f"Error: {str(e)}", 'danger')
    finally:
        cur.close()
        db.close()

    return redirect(url_for('kelola_paket'))

@app.route('/hapus_paket/<nama_paket>', methods=['GET'])
def hapus_paket(nama_paket):
    flash("Record Has Been Deleted Successfully")
    
    db = get_db_connection()
    cur = db.cursor()
    
    try:
        cur.execute("DELETE FROM jenis_paket WHERE jenis_laundry=%s", (nama_paket,))
        db.commit()
    except Exception as e:
        db.rollback()
        flash(f"Error: {str(e)}", 'danger')
    finally:
        cur.close()
        db.close()

    return redirect(url_for('kelola_paket'))



# Route data User
@app.route('/kelola_user/')
def kelola_user():
    db = get_db_connection()
    cursor = db.cursor()
    
    try:
        cursor.execute('SELECT * FROM login')
        result = cursor.fetchall()
    finally:
        cursor.close()
        db.close()

    return render_template('manajer/kelola_user.html', dt_admin=result)

@app.route('/tambah_user/', methods=['POST'])
def tambah_user():
    flash("Data Inserted Successfully")
    username = request.form['username']
    password = request.form['password']
    level = request.form['level']
    
    db = get_db_connection()
    cur = db.cursor()
    
    try:
        cur.execute('INSERT INTO login (username, password, level) VALUES (%s, %s, %s)', 
                    (username, password, level))
        db.commit()
    except Exception as e:
        db.rollback()
        flash(f"Error: {str(e)}", 'danger')
    finally:
        cur.close()
        db.close()

    return redirect(url_for('kelola_user'))

@app.route('/hapus_user/<username>', methods=['GET'])
def hapus_user(username):
    flash("Record Has Been Deleted Successfully")
    
    db = get_db_connection()
    cur = db.cursor()
    
    try:
        cur.execute("DELETE FROM login WHERE username=%s", (username,))
        db.commit()
    except Exception as e:
        db.rollback()
        flash(f"Error: {str(e)}", 'danger')
    finally:
        cur.close()
        db.close()

    return redirect(url_for('kelola_user'))

@app.route('/update_user/', methods=['GET', 'POST'])
def update_user():
    username = request.form['username']
    password = request.form['password']
    level = request.form['level']
    
    db = get_db_connection()
    cur = db.cursor()
    
    try:
        sql = '''UPDATE login
                SET password=%s, level=%s
                WHERE username=%s'''
        value = (password, level, username)
        cur.execute(sql, value)
        db.commit()
        flash("Data Updated Successfully")
    except Exception as e:
        db.rollback()
        flash(f"Error: {str(e)}", 'danger')
    finally:
        cur.close()
        db.close()

    return redirect(url_for('kelola_user'))

@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()