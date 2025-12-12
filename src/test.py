from motion_engine import MotionEngine

engine = MotionEngine(scene, bounds=bounds)
engine.add_random_walk("Tx1", [70, -10, 10], num_steps=3, step_size=10.0)
engine.add_random_walk("Tx2", [-260, 100, 10], num_steps=5, step_size=10.0)

padded_paths, max_steps = engine.create_path_matrix(padding_mode='pad_end')
