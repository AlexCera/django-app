from django.db import models
from django.contrib.auth.models import User

# Create your models here.
risk_qualifier = (
        ('0','?'),
        ('1','Aaa'),
        ('2','Aa1'),
        ('3','Aa2'),
        ('4','Aa3'),
        ('5','Baa1'),
        ('6','Baa2'),
        ('7','Baa3'),
    )

risk_type = (
        ('0', 'Pendiente'),
        ('1', 'Riesgo de crédito'),
        ('2', 'Riesgo de mercado'),
        ('3', 'Riesgo de liquidez'),
        ('4', 'Riesgo operativo'),
        ('5', 'Riesgo regulatorio'),
        ('6', 'Riesgo de reputación'),
    )

class Company(models.Model):
    name = models.CharField(blank=False,max_length=60,null=False)
    sector = models.CharField(blank=False,max_length=60,null=False)
    risk_qualifier = models.CharField(default='?',choices=risk_qualifier,null=False,max_length=1)
    risk_type = models.CharField(default=0,choices=risk_type,null=False,max_length=2)
    risk_rating = models.DecimalField(blank=False,null=False,decimal_places=2,max_digits=3)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

    def __str__(self):
        return self.name+ ' - ' + self.sector
    
    def risk_rating_percentage(self):
        return int(self.risk_rating * 100)
