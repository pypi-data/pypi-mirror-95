from distutils.core import setup

setup(
    name='django-campaign',
    version=__import__('campaign').__version__,
    description='A basic newsletter app for the Django webframework',
    long_description=open('README.rst').read(),
    author='Arne Brodowski',
    author_email='arne@rcs4u.de',
    license="BSD",
    url='https://github.com/arneb/django-campaign/',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    packages = (
        'campaign',
        'campaign.backends',
        'campaign.management',
        'campaign.management.commands',
        'campaign.migrations',
        'campaign.templatetags',
    ),
    package_data = {
        'campaign':
            [
                'templates/admin/campaign/blacklistentry/*.html',
                'templates/admin/campaign/campaign/*.html',
                'templates/admin/campaign/subscriberlist/*.html',
                'templates/campaign/*.html'
            ],
    }
)
