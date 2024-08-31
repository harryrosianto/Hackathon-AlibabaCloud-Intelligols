from enum import Enum
from models.role import RoleBase, RoleFullBase
from util.partial import optional


class RoleCreateSch(RoleBase):
    pass

class RoleSch(RoleFullBase):
    pass

@optional
class RoleUpdateSch(RoleBase):
    pass

class RoleEnum(str, Enum):
    admin = "ADMIN"
    farmer = "FARMER"
    buyer = "BUYER"
    argonomist = "ARGONOMIST"
    
# 1. Petani
# Fungsi Login: Petani dapat masuk ke aplikasi untuk mengakses fitur yang membantu mereka dalam proses penanaman, termasuk memasukkan data lingkungan, menerima rekomendasi dari AI, dan memantau kondisi tanam secara real-time.
# 2. Pembeli (Buyer)
# Fungsi Login: Pembeli dapat masuk ke aplikasi untuk memantau proses produksi kopi, melihat data real-time tentang kondisi tanam dan kualitas kopi, serta melakukan transaksi langsung dengan petani.
# 3. Administrator (Admin)
# Fungsi Login: Administrator memiliki akses ke pengelolaan sistem secara keseluruhan, termasuk manajemen pengguna (petani dan pembeli), pemantauan performa aplikasi, dan pengaturan konten atau fitur dalam aplikasi.
# 4. Agronomist/Subject Matter Expert (SME)
# Fungsi Login: SME bisa memiliki akses untuk meninjau data yang dikumpulkan, memberikan input atau rekomendasi tambahan, dan membantu dalam validasi model AI berdasarkan kondisi lapangan.