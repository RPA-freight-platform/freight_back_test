from app import db

class FreightInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    data_source = db.Column(db.String(20), nullable=False)
    plat_date = db.Column(db.String(20), nullable=False)
    valid_date = db.Column(db.String(20), nullable=False)
    
    pol_code = db.Column(db.String(10), nullable=False)
    pod_code = db.Column(db.String(10), nullable=False)
    lead_time = db.Column(db.Integer, nullable=False)
    bills = db.relationship('Bill', backref='freight_info', lazy=True)

class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tariff_group_code = db.Column(db.String(10), nullable=False)
    bill_name = db.Column(db.String(50), nullable=False)
    bill_div_code = db.Column(db.String(10), nullable=False)
    bill_unit = db.Column(db.String(10), nullable=False)
    cntr_size = db.Column(db.String(10), nullable=False)
    cntr_type = db.Column(db.String(10), nullable=False)
    currency_code = db.Column(db.String(10), nullable=False)
    bill_rate = db.Column(db.Float, nullable=False)
    freight_info_id = db.Column(db.Integer, db.ForeignKey('freight_info.id'), nullable=False)