import pickle
import zlib
from cryptography.fernet import Fernet

# Generate encryption key for secrets
key = Fernet.generate_key()
cipher_suite = Fernet(key)

config = {
    'version': '1.0',
    'environments': {
        'production': {
            'database': {
                'host': 'prod-db.example.com',
                'port': 5432,
                'name': 'prod_database',
                'user': 'prod_user',
                'password': cipher_suite.encrypt(b'prod_password').decode('utf-8'),  # Encrypted
            },
            'logging': {
                'level': 'INFO',
                'file': '/var/log/app/prod.log',
                'rotation': 'daily'
            },
            'cache': {
                'enabled': True,
                'redis_host': 'prod-redis.example.com',
                'redis_port': 6379,
                'redis_password': cipher_suite.encrypt(b'prod_redis_password').decode('utf-8'),  # Encrypted
            }
        },
        'development': {
            'database': {
                'host': 'localhost',
                'port': 5432,
                'name': 'dev_database',
                'user': 'dev_user',
                'password': 'dev_password',
            },
            'logging': {
                'level': 'DEBUG',
                'file': 'logs/dev.log',
                'rotation': 'size:10MB'
            },
            'cache': {
                'enabled': False,
                'redis_host': 'localhost',
                'redis_port': 6379,
                'redis_password': 'dev_redis_password',
            }
        }
    },
    'features': {
        'experimental': {
            'feature_one': True,
            'feature_two': False
        },
        'stable': {
            'feature_three': True,
            'feature_four': True
        }
    }
}

# Serialize and compress the data
compressed_data = zlib.compress(pickle.dumps(config))

# To write the binary config to a file
with open('complex_config.bin', 'wb') as f:
    f.write(compressed_data)

# To read and decompress the binary config from a file
with open('complex_config.bin', 'rb') as f:
    loaded_data = zlib.decompress(f.read())
    config = pickle.loads(loaded_data)
    print(config)
