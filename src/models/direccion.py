from sqlalchemy.types import UserDefinedType

class Direccion(UserDefinedType):
    def get_col_spec(self):
        return "direccion"

    def bind_processor(self, dialect):
        def process(value):
            if value is not None:
                # Usar formateo manual para asegurarse de que no hay comillas adicionales
                calle = value['calle']
                colonia = value['colonia']
                municipio = value['municipio']
                num_exterior = value['num_exterior']
                
                # Evita las comillas escapadas
                return f'({calle}, {colonia}, {municipio}, {num_exterior})'
            return None
        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            if value is not None:
                # Eliminar los paréntesis inicial y final y dividir por comas
                calle, colonia, municipio, num_exterior = value[1:-1].split(",")
                return {
                    "calle": calle.strip().strip('"'),
                    "colonia": colonia.strip().strip('"'),
                    "municipio": municipio.strip().strip('"'),
                    "num_exterior": num_exterior.strip().strip('"')
                }
            return None
        return process
