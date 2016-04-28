from setuptools import setup, find_packages

setup(
    name='django-simple-redis-admin',
    version='1.3.0',
    description='A django admin application to manage redis cache keys.',
    long_description=open('README.md').read(),
    author='Nicholas Serra',
    author_email='nick@528hazelwood.com',
    url='https://github.com/nicholasserra/django-simple-redis-admin',
    packages=find_packages(exclude=[]),
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    zip_safe=False,
)
