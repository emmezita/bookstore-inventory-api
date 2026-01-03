import requests
from decimal import Decimal, ROUND_HALF_UP
from django.utils import timezone
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class ExchangeRateService:
    """Servicio para obtener tasas de cambio desde API externa."""
    
    API_URL = "https://api.exchangerate-api.com/v4/latest/USD"
    TIMEOUT = 5  # segundos
    
    # Tasas por defecto en caso de fallo de la API
    DEFAULT_RATES = {
        'EUR': Decimal('0.92'),
        'GBP': Decimal('0.79'),
        'MXN': Decimal('17.15'),
        'COP': Decimal('3950.00'),
        'ARS': Decimal('875.00'),
        'CLP': Decimal('880.00'),
        'PEN': Decimal('3.72'),
        'BRL': Decimal('4.97'),
    }
    
    # Mapeo de código de país a moneda
    COUNTRY_TO_CURRENCY = {
        'ES': 'EUR',
        'FR': 'EUR',
        'DE': 'EUR',
        'IT': 'EUR',
        'GB': 'GBP',
        'UK': 'GBP',
        'US': 'USD',
        'MX': 'MXN',
        'CO': 'COP',
        'AR': 'ARS',
        'CL': 'CLP',
        'PE': 'PEN',
        'BR': 'BRL',
    }
    
    @classmethod
    def get_currency_for_country(cls, country_code: str) -> str:
        """Obtiene la moneda correspondiente a un código de país."""
        return cls.COUNTRY_TO_CURRENCY.get(country_code.upper(), 'USD')
    
    @classmethod
    def get_exchange_rate(cls, target_currency: str) -> tuple[Decimal, bool]:
        """
        Obtiene la tasa de cambio USD -> target_currency.
        
        Returns:
            tuple: (tasa_de_cambio, es_tasa_real)
            - es_tasa_real: True si viene de la API, False si es tasa por defecto
        """
        if target_currency == 'USD':
            return Decimal('1.00'), True
        
        try:
            response = requests.get(cls.API_URL, timeout=cls.TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            rates = data.get('rates', {})
            
            if target_currency in rates:
                rate = Decimal(str(rates[target_currency]))
                logger.info(f"Tasa obtenida de API: USD -> {target_currency} = {rate}")
                return rate, True
            else:
                logger.warning(f"Moneda {target_currency} no encontrada en API, usando tasa por defecto")
                return cls._get_default_rate(target_currency), False
                
        except requests.exceptions.Timeout:
            logger.error("Timeout al conectar con API de tasas de cambio")
            return cls._get_default_rate(target_currency), False
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al obtener tasas de cambio: {str(e)}")
            return cls._get_default_rate(target_currency), False
            
        except (KeyError, ValueError) as e:
            logger.error(f"Error al procesar respuesta de API: {str(e)}")
            return cls._get_default_rate(target_currency), False
    
    @classmethod
    def _get_default_rate(cls, currency: str) -> Decimal:
        """Retorna la tasa por defecto para una moneda."""
        return cls.DEFAULT_RATES.get(currency, Decimal('1.00'))


class PriceCalculatorService:
    """Servicio para calcular precios de venta."""
    
    DEFAULT_MARGIN = Decimal('0.40')  # 40%
    
    @classmethod
    def calculate_selling_price(
        cls,
        cost_usd: Decimal,
        country_code: str,
        margin: Decimal = None
    ) -> dict:
        """
        Calcula el precio de venta sugerido para un libro.
        
        Args:
            cost_usd: Costo en USD
            country_code: Código del país para determinar la moneda
            margin: Margen de ganancia (default 40%)
        
        Returns:
            dict con el detalle del cálculo
        """
        if margin is None:
            margin = cls.DEFAULT_MARGIN
        
        # Obtener moneda del país
        currency = ExchangeRateService.get_currency_for_country(country_code)
        
        # Obtener tasa de cambio
        exchange_rate, is_live_rate = ExchangeRateService.get_exchange_rate(currency)
        
        # Calcular costo en moneda local
        cost_local = (cost_usd * exchange_rate).quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP
        )
        
        # Aplicar margen de ganancia
        margin_multiplier = Decimal('1') + margin
        selling_price = (cost_local * margin_multiplier).quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP
        )
        
        return {
            'cost_usd': cost_usd,
            'exchange_rate': exchange_rate,
            'cost_local': cost_local,
            'margin_percentage': int(margin * 100),
            'selling_price_local': selling_price,
            'currency': currency,
            'is_live_rate': is_live_rate,
            'calculation_timestamp': timezone.now(),
        }