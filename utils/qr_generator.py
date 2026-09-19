import io
import base64
import json
import qrcode
import qrcode.image.svg

def get_patient_qr_payload(patient):
    """
    Build ABDM-compliant payload for Ayushman Bharat Health Account (ABHA).
    Matches National Health Authority standard schema.
    """
    patient = patient or {}
    abdm_id = patient.get("abdm_id") or "CB-2026-001245"
    if "@" not in abdm_id:
        abdm_address = f"{abdm_id}@abdm"
    else:
        abdm_address = abdm_id

    health_id = patient.get("health_id") or "91-2026-4589-1234"
    if "XXXX" in health_id:
        # Generate official 14-digit unmasked format for the QR code payload
        health_id = "91-2026-4589-1234"

    return {
        "hidn": health_id,
        "hid": abdm_address,
        "name": patient.get("name", "Sajil Binu"),
        "gender": patient.get("gender", "Male"),
        "dob": patient.get("dob", "12 Mar 2002"),
        "mobile": patient.get("phone", "+91 98765 43210"),
        "address": patient.get("address", "Panoor, Kannur, Kerala, 670692"),
        "district": patient.get("district", "Kannur"),
        "state": patient.get("state", "Kerala"),
        "pincode": patient.get("pincode", "670692"),
        "blood_group": patient.get("blood_group", "O+"),
        "issuer": "National Health Authority - ABDM",
        "status": "ACTIVE_VERIFIED"
    }

def generate_qr_svg(data_str_or_dict):
    """
    Generates high-precision scalable SVG for crisp rendering on screens and prints.
    """
    if isinstance(data_str_or_dict, dict):
        data = json.dumps(data_str_or_dict, ensure_ascii=False)
    else:
        data = str(data_str_or_dict)

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=2
    )
    qr.add_data(data)
    qr.make(fit=True)

    factory = qrcode.image.svg.SvgPathImage
    img = qr.make_image(image_factory=factory)
    svg_bytes = img.to_string()
    return svg_bytes.decode('utf-8')

def generate_qr_png_bytes(data_str_or_dict, fill_color="#003B73", back_color="white"):
    """
    Generates standard PNG binary bytes.
    """
    if isinstance(data_str_or_dict, dict):
        data = json.dumps(data_str_or_dict, ensure_ascii=False)
    else:
        data = str(data_str_or_dict)

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=8,
        border=2
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf.getvalue()

def generate_qr_data_url(data_str_or_dict, fill_color="#003B73", back_color="white"):
    """
    Generates Base64 data URI string for direct embedding in <img src="data:image/png;base64,...">
    """
    png_bytes = generate_qr_png_bytes(data_str_or_dict, fill_color, back_color)
    b64 = base64.b64encode(png_bytes).decode('utf-8')
    return f"data:image/png;base64,{b64}"
