from distutils.core import setup

setup(
    # How you named your package folder (MyLib)
    name="rabbitmq_flask",
    packages=["rabbitmq_flask"],  # Chose the same as "name"
    # Start with a small number and increase it with every change you make
    version="1.0.1",
    # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    license="MIT",
    # Give a short description about your library
    description="Adapter for RabbitMQ and flask",
    author="Arif Sajal",  # Type in your name
    author_email="arif.is.sajal@gmail.com",  # Type in your E-Mail
    # Provide either the link to your github or to your website
    url="https://github.com/arif-sajal/rabbitmq-flask",
    # I explain this later on
    download_url="https://github.com/arif-sajal/rabbitmq-flask/archive/0.1.tar.gz",
    # Keywords that define your package best
    keywords=["FLASK", "PIKA", "RABBITMQ", "MESSAGEQUEUE"],
    install_requires=[  # I get to this in a second
        "Flask>=1.1.1",
        "pika>=1.2.0",
        "retry>=0.9.2",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
