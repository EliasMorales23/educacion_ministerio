# routers.py

class SecondaryDBRouter:
    """
    Controla que todos los modelos de 'mi_app_datos_secundarios' 
    usen la BD 'secundaria'.
    """
    
    # Lista de apps que deben usar la BD secundaria
    route_apps = {'evaluaciones_educativas'} 

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_apps:
            return 'bd_evaluacion'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_apps:
            return 'bd_evaluacion'
        return 'default'

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # Asegura que las migraciones de esta app solo corran en su BD asignada
        if app_label in self.route_apps:
            return db == 'bd_evaluacion'
        return db == 'default'