emnlp18:
	python3 -m dtsr.bin.train experiments_emnlp18/synth.ini
	python3 -m dtsr.bin.train experiments_emnlp18/natstor.ini
	python3 -m dtsr.bin.predict experiments_emnlp18/natstor.ini -a sampling -p train
	python3 -m dtsr.bin.predict experiments_emnlp18/natstor.ini -a sampling -p dev
	python3 -m dtsr.bin.predict experiments_emnlp18/natstor.ini -a sampling -p test
	python3 -m dtsr.bin.train experiments_emnlp18/dundee.ini
	python3 -m dtsr.bin.predict experiments_emnlp18/dundee.ini -a sampling -p train
	python3 -m dtsr.bin.predict experiments_emnlp18/dundee.ini -a sampling -p dev
	python3 -m dtsr.bin.predict experiments_emnlp18/dundee.ini -a sampling -p test
	python3 -m dtsr.bin.train experiments_emnlp18/ucl.ini
	python3 -m dtsr.bin.predict experiments_emnlp18/ucl.ini -a sampling -p train
	python3 -m dtsr.bin.predict experiments_emnlp18/ucl.ini -a sampling -p dev
	python3 -m dtsr.bin.predict experiments_emnlp18/ucl.ini -a sampling -p test
	python3 -m dtsr.bin.compare_to_baselines -t experiments_emnlp18/natstor.ini experiments_emnlp18/dundee.ini experiments_emnlp18/ucl.ini -p test

reading:
	python3 -m dtsr.bin.train experiments_reading/dundee.ini -m DTSR.*
	python3 -m dtsr.bin.predict experiments_reading/dundee.ini -a sampling -p train -m DTSR.*
	python3 -m dtsr.bin.predict experiments_reading/dundee.ini -a sampling -p dev -m DTSR.*
	python3 -m dtsr.bin.convolve experiments_reading/dundee.ini -a sampling -p train -m DTSR.*
	python3 -m dtsr.bin.convolve experiments_reading/dundee.ini -a sampling -p dev -m DTSR.*
	python3 -m dtsr.bin.train experiments_reading/ucl.ini -m DTSR.*
	python3 -m dtsr.bin.predict experiments_reading/ucl.ini -a sampling -p train -m DTSR.*
	python3 -m dtsr.bin.predict experiments_reading/ucl.ini -a sampling -p dev -m DTSR.*
	python3 -m dtsr.bin.convolve experiments_reading/ucl.ini -a sampling -p train -m DTSR.*
	python3 -m dtsr.bin.convolve experiments_reading/ucl.ini -a sampling -p dev -m DTSR.*
