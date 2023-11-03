import matlab.engine

eng = matlab.engine.start_matlab()
eng.run('simpleRoad.m', nargout=0)
eng.quit()
