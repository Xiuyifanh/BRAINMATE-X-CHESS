from setuptools import setup, find_packages

setup(
    name="brainmate_chess",
    version="1.1.0",
    description="AI-powered chess assistant for Starknet integration",
    author="NIHAAR RAUT",
    author_email="emiratenihaar@gmail.com",
    packages=find_packages(),
    install_requires=[
        "chess",
        "stockfish",
    ],
    extras_require={
        "lichess": ["berserk"],
    },
    entry_points={
        "console_scripts": [
            "chess-ai=chess_agent.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
)
