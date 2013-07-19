from django.db import models
from django.conf import settings
import MySQLdb as mdb
import hashlib, sys

class Usuario(models.Model):
    nombre = models.CharField(max_length=25)
    email = models.EmailField()
    def __unicode__(self):
        return "%s"%self.nombre
    def get_absolute_url(self):
        return "/listas/usuarios/%d/"%self.id
    
class Sitio(models.Model):
    dominio = models.CharField(max_length=100)
    nombre = models.CharField("el nombre del sitio, se usa para saber el nombre de la BBDD",max_length=25)
    def __unicode__(self):
        return "%s"%self.nombre
    def get_absolute_url(self):
        return "/listas/sitios/%d/"%self.id


class Lista(models.Model):
    sitio = models.ForeignKey(Sitio,blank=True)
    nombre = models.CharField(max_length=25)
    usuarios =  models.ManyToManyField(Usuario,blank=True)
    def __unicode__(self):
        return "%s"%self.nombre
    def get_absolute_url(self):
        return "/listas/%d/"%self.id
	def save(self):
		print "Somos la funcion personal de guardar"
		if self.pk is None:
			print "Es la primera vez que nos salvan.."
		super(Lista, self).save()

def sincronizar_sitios_listas():
	for sitio in Sitio.objects.all():
		print("Vamos a sincronizar las listas de %s"%sitio.nombre)
		nombre_bbdd = "phplist_%s"%sitio.nombre
		##El id de el usuario no inicializamos a 1 en cada sitio
		user_id=1
		try:
			con = mdb.connect(settings.BBDD_SERVER, settings.BBDD_USER, settings.BBDD_PASSWD, nombre_bbdd)
			print "\tConectado a la BBDD"
			cur = con.cursor()
			print "\tBorrando las listas"
			sql = "TRUNCATE  phplist_list"
			cur.execute(sql)
			print "\tBorrando los usuarios"
			sql = "TRUNCATE  phplist_user_user"
			cur.execute(sql)
			print "\tBorrando las asociaciones usurios listas"
			sql = "TRUNCATE  phplist_listuser"
			cur.execute(sql)
			
			for lista in sitio.lista_set.all():
				if lista.nombre == "":
					continue
				print "\tVamos a trabajar con la lista...%s"%lista.nombre
				listorder="0"
				prefix="NULL"
				rssfeed="NULL"
				active="1"
				owner="1"
				sql = "INSERT INTO phplist_list VALUES("+str(lista.id)+",'"+lista.nombre+"','"+lista.nombre+"',NOW() ,"+listorder+","+prefix+","+rssfeed+",NOW(),"+active+","+owner+")"
				cur.execute(sql)

				for usuario in lista.usuarios.all():
					print "\tVamos a anadir el usuario %s"%usuario.nombre
					sql="SELECT id FROM phplist_user_user WHERE email='"+str(usuario.email)+"'"
					cur.execute(sql)
					res = cur.fetchall()
					if len(res) > 0:
						print "\t\tYa existe el user %s"%res[0]
						temp_user_id="%s"%res[0]
						sql="INSERT INTO phplist_listuser VALUES("+temp_user_id+","+str(lista.id)+",NOW(),NOW())"
						#print sql
						cur.execute(sql)
					else:
						print "\t\tCreamos user nuevo"
						h = hashlib.sha1(usuario.email+settings.SECRET_KEY)
						h = h.hexdigest()
						sql="INSERT INTO phplist_user_user VALUES("+str(user_id)+",'"+usuario.email+"',1,0,0,NOW(),NOW(),'"+str(h)+"',1,NULL,NULL,NULL,NULL,0,NULL,NULL)"
						cur.execute(sql)
						user_id=user_id+1
						sql="INSERT INTO phplist_listuser VALUES("+str(user_id)+","+str(lista.id)+",NOW(),NOW())"
						#print sql
						cur.execute(sql)
					
			print "Hemos terminado con el sitio %s"%sitio.nombre
			con.close()
		except mdb.Error, e:
			print "Error %d: %s" % (e.args[0], e.args[1])
			sys.exit(1)
