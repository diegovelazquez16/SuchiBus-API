from sqlalchemy.types import UserDefinedType

class Direccion(UserDefinedType):
    def get_col_spec(self):
        return "direccion"

    def bind_processor(self, dialect):
        def process(value):
            if value is not None:
                calle = value['calle']
                colonia = value['colonia']
                municipio = value['municipio']
                num_exterior = value['num_exterior']
                
                return f'({calle}, {colonia}, {municipio}, {num_exterior})'
            return None
        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            if value is not None:
                calle, colonia, municipio, num_exterior = value[1:-1].split(",")
                return {
                    "calle": calle.strip().strip('"'),
                    "colonia": colonia.strip().strip('"'),
                    "municipio": municipio.strip().strip('"'),
                    "num_exterior": num_exterior.strip().strip('"')
                }
            return None
        return process
