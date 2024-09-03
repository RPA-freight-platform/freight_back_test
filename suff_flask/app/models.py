from app import db
from datetime import datetime

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

# 데이터 조회 시 셀렉박스 선택을 위한 portcode 정보
class PortCodeItem(db.Model):
    __tablename__ = 'port_code_item'

    portCode = db.Column(db.String(50), primary_key=True, unique=True, nullable=False, comment='포트 코드')
    portName = db.Column(db.String(50), nullable=True, comment='포트명')
    portNameKor = db.Column(db.String(50), nullable=True, comment='포트 한글명')
    nationCode = db.Column(db.String(50), nullable=True, comment='국가 코드')
    continent = db.Column(db.String(50), nullable=True, comment='대륙 정보')
    region = db.Column(db.String(50), nullable=True, comment='권역')
    latitude = db.Column(db.String(50), nullable=True, comment='위도')
    longitude = db.Column(db.String(50), nullable=True, comment='경도')
    cargoTypes = db.Column(db.String(100), nullable=True, comment='터미널 기능')
    nearByPort_1 = db.Column(db.String(10), nullable=True, comment='인근항구_1')
    nearByPort_2 = db.Column(db.String(10), nullable=True, comment='인근항구_2')
    nearByPort_3 = db.Column(db.String(10), nullable=True, comment='인근항구_3')
    nearByPort_4 = db.Column(db.String(10), nullable=True, comment='인근항구_4')
    nearByAirport_1 = db.Column(db.String(100), nullable=True, comment='인근공항1')
    nearByAirportKm_1 = db.Column(db.String(100), nullable=True, comment='인근공항거리1')
    nearByAirport_2 = db.Column(db.String(100), nullable=True, comment='인근공항2')
    nearByAirportKm_2 = db.Column(db.String(100), nullable=True, comment='인근공항거리2')
    nearByAirport_3 = db.Column(db.String(100), nullable=True, comment='인근공항3')
    nearByAirportKm_3 = db.Column(db.String(100), nullable=True, comment='인근공항거리3')
    nearByAirport_4 = db.Column(db.String(100), nullable=True, comment='인근공항4')
    nearByAirportKm_4 = db.Column(db.String(100), nullable=True, comment='인근공항거리4')
    itemOrder = db.Column(db.Integer, default=1, nullable=False, comment='정렬 순서')
    majorYN = db.Column(db.String(1), default='N', nullable=True, comment='주요 항구 여부')
    delYN = db.Column(db.String(1), default='N', nullable=False, comment='삭제 여부')
    regKey = db.Column(db.String(50), nullable=True, comment='최초 등록자 통합유일키')
    regDate = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, comment='최초 등록 일시')
    modKey = db.Column(db.String(50), nullable=True, comment='최종 수정자 통합유일키')
    modDate = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment='최종 수정 일시')

    def __repr__(self):
        return f'{self.portCode}'