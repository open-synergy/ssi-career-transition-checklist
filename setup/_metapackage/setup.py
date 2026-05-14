import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-open-synergy-ssi-career-transition-checklist",
    description="Meta package for open-synergy-ssi-career-transition-checklist Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-ssi_career_transition_checklist',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
