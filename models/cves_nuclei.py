from database.mysql_client import db


class CvesNuclei(db.Model):
    __tablename__ = "cves_nuclei"

    id = db.Column(db.String(32), primary_key=True, comment="uuid 主键")
    cve_id = db.Column(db.String(20), unique=True, nullable=False, comment="nuclei-template 中存在模板的 cve id")
    cve_yaml_path = db.Column(db.String(100), unique=True, nullable=False, comment="cve 对应模板文件的使用路径")
    created_at = db.Column(db.DateTime, default=db.func.now(), comment="创建时间")
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now(), comment="更新时间")
