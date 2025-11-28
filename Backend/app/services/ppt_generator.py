import os
from io import BytesIO
from datetime import datetime, date
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.exc import ProgrammingError, OperationalError

# --- MODEL IMPORTS ---
from app.models.tank_header import Tank
from app.models.tank_details import TankDetails
from app.models.tank_images import TankImage
from app.models.tank_regulations import TankRegulation
from app.models.regulations_master import RegulationsMaster
from app.models.cargo_tank import CargoTankTransaction
from app.models.cargo_master import CargoTankMaster
from app.models.tank_certificate import TankCertificate
from app.models.tank_drawings import TankDrawing
from app.models.valve_test_report import ValveTestReport

# --- CONFIGURATION ---
THEME_COLOR = RGBColor(0, 51, 102)
HEADER_TEXT = "Smart-Gas Pte Ltd"
SUB_HEADER_TEXT = "140 Paya Lebar Road #05-21, AZ Building, Singapore 409015\nTel : (65) 6848 1040 / Fax : (65) 6848 2173"

# --- PATH RESOLUTION ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SEARCH_ROOTS = [
    r"E:\ISOTank-Mobile 1\Backend",   
    r"E:\ISO-Tank\Backend",            
    PROJECT_ROOT                       
]

IMAGE_TYPE_MAP = {
    "frontview": "Front View", "rearview": "Rear View", "topview": "Top View",
    "undersideview": "Underside View", "frontlhview": "Front LH View",
    "rearlhview": "Rear LH View", "frontrhview": "Front RH View",
    "rearrhview": "Rear RH View", "lhsideview": "LH Side View",
    "rhsideview": "RH Side View", "valvessectionview": "Valves Section",
    "safetyvalve": "Safety Valve", "levelpressuregauge": "Level/Pressure Gauge",
    "vacuumreading": "Vacuum Reading"
}

def resolve_path(file_path, tank_number):
    if not file_path: return None
    filename = os.path.basename(file_path)
    if os.path.exists(file_path): return file_path
    clean_rel = file_path.replace("\\", "/")
    if "uploads/" in clean_rel: clean_rel = clean_rel.split("uploads/", 1)[1] 
    
    for root in SEARCH_ROOTS:
        candidates = [
            os.path.join(root, "uploads", clean_rel),
            os.path.join(root, "uploads", "tank_images_mobile", tank_number, filename),
            os.path.join(root, "uploads", "drawings", tank_number, filename),
            os.path.join(root, "uploads", "certificates", tank_number, filename),
            os.path.join(root, "uploads", "valve_reports", tank_number, filename),
            os.path.join(root, "uploads", "drawings", filename),
            os.path.join(root, "uploads", "certificates", filename)
        ]
        for path in candidates:
            if os.path.exists(path): return path
    return None

def format_value(value, suffix=""):
    if value is None or value == "": return "-"
    if isinstance(value, bool): return "Yes" if value else "No"
    if isinstance(value, (datetime, date)): return value.strftime("%d-%b-%Y")
    try:
        float_val = float(value)
        if float_val.is_integer(): return f"{int(float_val):,} {suffix}".strip()
        return f"{float_val:,.2f} {suffix}".strip()
    except: return f"{str(value)} {suffix}".strip()

def add_custom_header(slide, title_text=""):
    left = Inches(1)
    txBox = slide.shapes.add_textbox(left, Inches(0.2), Inches(8), Inches(0.5))
    p = txBox.text_frame.paragraphs[0]; p.text = HEADER_TEXT
    p.font.bold = True; p.font.size = Pt(24); p.font.color.rgb = THEME_COLOR; p.alignment = PP_ALIGN.CENTER
    txBox = slide.shapes.add_textbox(left, Inches(0.6), Inches(8), Inches(0.6))
    p = txBox.text_frame.paragraphs[0]; p.text = SUB_HEADER_TEXT
    p.font.size = Pt(10); p.font.color.rgb = RGBColor(0, 0, 0); p.alignment = PP_ALIGN.CENTER
    if title_text:
        txBox = slide.shapes.add_textbox(Inches(0.5), Inches(1.3), Inches(8), Inches(0.4))
        p = txBox.text_frame.paragraphs[0]; p.text = title_text
        p.font.bold = True; p.font.size = Pt(16); p.font.color.rgb = THEME_COLOR

def create_kv_slide(prs, tank_number, title, data_pairs):
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    add_custom_header(slide, f"{tank_number} - {title}")
    rows = len(data_pairs); cols = 2
    left = Inches(1.5); top = Inches(1.8); width = Inches(7); height = Inches(0.3 * rows)
    table = slide.shapes.add_table(rows, cols, left, top, width, height).table
    table.columns[0].width = Inches(2.5); table.columns[1].width = Inches(4.5)
    for i, (label, value) in enumerate(data_pairs):
        cell_lbl = table.cell(i, 0); cell_lbl.text = str(label)
        cell_lbl.text_frame.paragraphs[0].font.bold = True
        cell_lbl.text_frame.paragraphs[0].font.size = Pt(12)
        cell_val = table.cell(i, 1); cell_val.text = str(value)
        cell_val.text_frame.paragraphs[0].font.size = Pt(12)

def create_table_slide(prs, tank_number, title, headers, data_rows):
    if not data_rows: return
    chunk_size = 12
    for i in range(0, len(data_rows), chunk_size):
        chunk = data_rows[i:i + chunk_size]
        slide = prs.slides.add_slide(prs.slide_layouts[5])
        header_suffix = f" ({int(i/chunk_size)+1})" if len(data_rows) > chunk_size else ""
        add_custom_header(slide, f"{tank_number} - {title}{header_suffix}")
        rows = len(chunk) + 1; cols = len(headers)
        left = Inches(0.5); top = Inches(1.8); width = Inches(9); height = Inches(0.3 * rows)
        table = slide.shapes.add_table(rows, cols, left, top, width, height).table
        for j, h_text in enumerate(headers):
            cell = table.cell(0, j); cell.text = h_text
            cell.fill.solid(); cell.fill.fore_color.rgb = THEME_COLOR
            p = cell.text_frame.paragraphs[0]; p.font.bold = True; p.font.color.rgb = RGBColor(255, 255, 255); p.font.size = Pt(11)
        for r_idx, row_data in enumerate(chunk):
            for c_idx, value in enumerate(row_data):
                cell = table.cell(r_idx + 1, c_idx); cell.text = str(value)
                cell.text_frame.paragraphs[0].font.size = Pt(10)

def add_image_sequence(prs, tank_number, image_list, section_title):
    valid_items = []
    for item in image_list:
        if not item['path']: continue
        real_path = resolve_path(item['path'], tank_number)
        if real_path: valid_items.append({'path': real_path, 'label': item['label']})
        else: valid_items.append({'path': None, 'label': item['label'], 'original': item['path']})
    if not valid_items: return
    current_slide = None
    for i, img_item in enumerate(valid_items):
        path = img_item.get('path'); label = img_item.get('label')
        if i % 2 == 0:
            current_slide = prs.slides.add_slide(prs.slide_layouts[5])
            add_custom_header(current_slide, f"{tank_number} - {section_title}")
        is_top = (i % 2 == 0)
        base_top = Inches(1.8) if is_top else Inches(4.5)
        label_top = Inches(1.6) if is_top else Inches(4.3)
        label_box = current_slide.shapes.add_textbox(Inches(1), label_top, Inches(8), Inches(0.3))
        label_box.text_frame.text = label
        label_box.text_frame.paragraphs[0].font.bold = True; label_box.text_frame.paragraphs[0].font.size = Pt(12)
        if path:
            ext = os.path.splitext(path)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif']:
                err_box = current_slide.shapes.add_textbox(Inches(1), base_top, Inches(4), Inches(1))
                err_box.text_frame.text = f"[PDF/Doc: {os.path.basename(path)}]"
                err_box.text_frame.paragraphs[0].font.color.rgb = RGBColor(0, 0, 0)
            else:
                try:
                    pic = current_slide.shapes.add_picture(path, Inches(1), base_top, height=Inches(2.5))
                    if pic.width > Inches(8):
                        ratio = Inches(8) / pic.width; pic.width = Inches(8); pic.height = int(pic.height * ratio)
                except Exception:
                    err_box = current_slide.shapes.add_textbox(Inches(1), base_top, Inches(4), Inches(1))
                    err_box.text_frame.text = "[Error Rendering Image]"; err_box.text_frame.paragraphs[0].font.color.rgb = RGBColor(255, 0, 0)
        else:
            err_box = current_slide.shapes.add_textbox(Inches(1), base_top, Inches(5), Inches(1))
            err_box.text_frame.text = f"[Image Not Found]\nPath: {img_item.get('original')}"; err_box.text_frame.paragraphs[0].font.color.rgb = RGBColor(255, 0, 0)

# ==============================================================================
# MAIN GENERATOR
# ==============================================================================
def create_presentation(db: Session, tank_id: int) -> BytesIO:
    tank = db.query(Tank).filter(Tank.id == tank_id).first()
    d = db.query(TankDetails).filter(TankDetails.tank_id == tank_id).first()
    if not tank or not d: raise ValueError("Tank Details not found")

    regs = db.query(TankRegulation, RegulationsMaster).outerjoin(RegulationsMaster, TankRegulation.regulation_id == RegulationsMaster.id).filter(TankRegulation.tank_id == tank_id).all()
    cargos = db.query(CargoTankTransaction, CargoTankMaster).join(CargoTankMaster, CargoTankTransaction.cargo_reference == CargoTankMaster.id).filter(CargoTankTransaction.tank_id == tank_id).all()
    certs = db.query(TankCertificate).filter(TankCertificate.tank_id == tank_id).all()
    drawings = db.query(TankDrawing).filter(TankDrawing.tank_id == tank_id).all()
    valves = db.query(ValveTestReport).filter(ValveTestReport.tank_id == tank_id).all()
    
    print(f"DEBUG: Searching inspection for Tank ID: {tank_id}, Number: {tank.tank_number}")
    
    # 1. FETCH INSPECTION (Safe Query)
    insp_sql = text("""
        SELECT * FROM tank_inspection_details 
        WHERE tank_id = :tid OR tank_number = :tn 
        ORDER BY inspection_date DESC LIMIT 1
    """)
    insp = db.execute(insp_sql, {"tid": tank_id, "tn": tank.tank_number}).mappings().first()
    
    checklist_rows = []
    todo_rows = []
    insp_images = []

    if insp:
        print(f"DEBUG: Found Inspection ID: {insp['inspection_id']}")
        iid = insp['inspection_id']
        
        # 2. FETCH CHECKLIST (With Error Handling for Missing Table)
        try:
            sql_chk = text("SELECT job_name, sub_job_description, status, comment FROM inspection_checklist WHERE inspection_id = :iid ORDER BY id ASC")
            checklist_data = db.execute(sql_chk, {"iid": iid}).fetchall()
            for r in checklist_data: checklist_rows.append([r[0], r[1], r[2] or "-", r[3] or "-"])
        except (ProgrammingError, OperationalError) as e:
            print(f"WARNING: Skipping Checklist - Table missing or error: {e}")

        # 3. FETCH TO-DO (With Error Handling for Missing Table)
        try:
            sql_todo = text("SELECT job_name, sub_job_description, status, comment FROM to_do_list WHERE inspection_id = :iid ORDER BY id ASC")
            todo_data = db.execute(sql_todo, {"iid": iid}).fetchall()
            for r in todo_data: todo_rows.append([r[0], r[1], r[2] or "Faulty", r[3] or "-"])
        except (ProgrammingError, OperationalError) as e:
             print(f"WARNING: Skipping To-Do List - Table missing or error: {e}")

        # 4. FETCH IMAGES (With Error Handling)
        try:
            img_sql = text("SELECT image_type, image_path FROM tank_images WHERE inspection_id = :iid ORDER BY id ASC")
            img_data = db.execute(img_sql, {"iid": iid}).fetchall()
            for r in img_data:
                readable_label = IMAGE_TYPE_MAP.get(r[0], str(r[0]).title().replace("_", " "))
                insp_images.append({'path': r[1], 'label': readable_label})
        except Exception as e:
            print(f"WARNING: Error fetching inspection images: {e}")
    else:
        print("DEBUG: NO INSPECTION FOUND.")
    
    # Fallback to tank header images if no inspection images
    if not insp_images:
        tank_images = db.query(TankImage).filter(TankImage.tank_number == tank.tank_number).all()
        for img in tank_images:
             readable_label = IMAGE_TYPE_MAP.get(img.image_type, (img.image_type or "").title())
             insp_images.append({'path': img.image_path, 'label': readable_label})

    # --- SLIDES CREATION ---
    prs = Presentation()

    slide_1_data = [("Tank Number", tank.tank_number), ("Manufacturer", d.mfgr), ("Date of Mfg", format_value(d.date_mfg)), ("Lease", format_value(d.lease)), ("UN ISO Code", d.un_iso_code), ("Size", d.size), ("Tare Weight", format_value(d.tare_weight_kg, "kg")), ("Gross Weight", format_value(d.gross_kg, "kg")), ("Net Weight", format_value(d.net_kg, "kg")), ("MGW", format_value(d.mgw_kg, "kg")), ("MPL", format_value(d.mpl_kg, "kg"))]
    create_kv_slide(prs, tank.tank_number, "General Identity & Weights", slide_1_data)

    slide_2_data = [("Capacity", format_value(d.capacity_l, "L")), ("MAWP", format_value(d.mawp, "Bar")), ("Working Pressure", format_value(d.working_pressure, "Bar")), ("Design Temp", d.design_temperature), ("Vessel Material", d.vesmat), ("PV Code", d.pv_code)]
    create_kv_slide(prs, tank.tank_number, "Technical Specifications", slide_2_data)

    slide_3_data = [("Frame Type", d.frame_type), ("Cabinet Type", d.cabinet_type), ("Color", d.color_body_frame), ("Pump Type", d.pump_type), ("Remarks", d.remark)]
    create_kv_slide(prs, tank.tank_number, "Construction Details", slide_3_data)
    
    # SLIDE 4: LATEST INSPECTION SUMMARY
    if insp:
        insp_data = [
            ("Report No", insp['report_number']), ("Inspection Date", format_value(insp['inspection_date'])),
            ("Status", insp['status_id']), ("Type", insp['inspection_type_id']),
            ("Location", insp['location_id']), ("Inspector", insp['created_by']),
            ("Safety Valve Brand", insp['safety_valve_brand_id']), ("Safety Valve Model", insp['safety_valve_model_id']),
            ("Notes", insp['notes'])
        ]
        create_kv_slide(prs, tank.tank_number, "Latest Inspection Summary", insp_data)

    reg_rows = [[r.regulation_name, format_value(t.initial_approval_no), format_value(t.imo_type), format_value(t.safety_standard), format_value(t.country_registration)] for t, r in regs]
    create_table_slide(prs, tank.tank_number, "Regulations", ["Regulation", "Approval", "IMO", "Safety", "Country"], reg_rows)

    cargo_rows = [[m.cargo_reference, format_value(c.density), format_value(c.loading_parts), format_value(c.compatability_notes)] for c, m in cargos]
    create_table_slide(prs, tank.tank_number, "Approved Cargos", ["Cargo", "Density", "Parts", "Notes"], cargo_rows)
    
    cert_rows = [[c.certificate_number, format_value(c.inspection_agency), format_value(c.insp_2_5y_date), format_value(c.next_insp_date)] for c in certs]
    create_table_slide(prs, tank.tank_number, "Certificates", ["Cert No", "Agency", "Insp Date", "Next Due"], cert_rows)
    
    create_table_slide(prs, tank.tank_number, "Inspection Checklist", ["Category", "Check Item", "Status", "Comment"], checklist_rows)
    create_table_slide(prs, tank.tank_number, "Faulty Items / To-Do List", ["Category", "Fault", "Status", "Action/Comment"], todo_rows)

    add_image_sequence(prs, tank.tank_number, insp_images, "Inspection Photos")
    cert_imgs = [{'path': c.certificate_file, 'label': f"Cert: {c.certificate_number}"} for c in certs if c.certificate_file]
    add_image_sequence(prs, tank.tank_number, cert_imgs, "Certificate Documents")
    draw_imgs = [{'path': dr.file_path, 'label': f"Drawing: {dr.drawing_type}"} for dr in drawings if dr.file_path]
    add_image_sequence(prs, tank.tank_number, draw_imgs, "Technical Drawings")
    valve_imgs = [{'path': v.inspection_report_file, 'label': f"Report: {format_value(v.test_date)}"} for v in valves if v.inspection_report_file]
    add_image_sequence(prs, tank.tank_number, valve_imgs, "Valve Test Documents")

    output = BytesIO()
    prs.save(output)
    output.seek(0)
    return output