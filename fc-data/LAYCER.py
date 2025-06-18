from cryptography import x509
from cryptography.hazmat.backends import default_backend

# Đường dẫn tới file mới
cert_path = "d:\\certificate_chain.pem"

# Đọc nội dung file
with open(cert_path, "rb") as f:
    pem_data = f.read()

# Tách các chứng chỉ trong chuỗi PEM và kiểm tra
certs = []
for cert_pem in pem_data.split(b"-----END CERTIFICATE-----"):
    cert_pem = cert_pem.strip()
    if cert_pem:
        cert_pem += b"\n-----END CERTIFICATE-----\n"
        try:
            cert = x509.load_pem_x509_certificate(cert_pem, default_backend())
            certs.append(cert)
        except Exception as e:
            certs.append(f"Lỗi: {e}")

certs_summary = [str(c) if isinstance(c, Exception) else f"✅ Issuer: {c.issuer.rfc4514_string()}" for c in certs]
certs_summary
