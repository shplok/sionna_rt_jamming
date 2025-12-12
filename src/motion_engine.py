# motion_engine.py
import numpy as np

def generate_random_walk(starting_position, num_steps, step_size, 
                         time_step=0.1, z_fixed=True, bounds=None, random_seed=None):

    if random_seed is not None:
        np.random.seed(random_seed)
    
    path = np.zeros((num_steps, 3))
    path[0] = starting_position
    
    for step in range(1, num_steps):
        direction = np.random.randn(3)
        if z_fixed:
            direction[2] = 0
        direction = direction / np.linalg.norm(direction)
        direction = direction * step_size
        new_position = path[step - 1] + direction
        
        if bounds is not None:
            for i, axis in enumerate(['x', 'y', 'z']):
                if axis in bounds:
                    new_position[i] = np.clip(new_position[i], bounds[axis][0], bounds[axis][1])
        
        path[step] = new_position
    
    distances = np.linalg.norm(np.diff(path, axis=0), axis=1)
    total_distance = np.sum(distances)
    avg_velocity = step_size / time_step if time_step > 0 else 0
    
    metadata = {
        'total_distance': total_distance,
        'avg_velocity': avg_velocity,
        'time_step': time_step,
        'num_steps': num_steps,
        'step_size': step_size
    }
    
    return path, metadata


class MotionEngine:

    def __init__(self, scene, bounds=None):
        self.scene = scene
        self.bounds = bounds
        self.jammer_paths = {}
        self.jammer_metadata = {}
        
    def add_random_walk(self, jammer_id, starting_position, num_steps, 
                        step_size, time_step=0.1, z_fixed=True, random_seed=None):

        path, metadata = generate_random_walk(
            starting_position=starting_position,
            num_steps=num_steps,
            step_size=step_size,
            time_step=time_step,
            z_fixed=z_fixed,
            bounds=self.bounds,
            random_seed=random_seed
        )
        
        self.jammer_paths[jammer_id] = path
        self.jammer_metadata[jammer_id] = metadata
        
        print(f"Generated path for '{jammer_id}': Total distance: {metadata['total_distance']:.2f} m, Avg velocity: {metadata['avg_velocity']:.2f} m/s")
        
        return path, metadata
    
    def get_position_at_step(self, jammer_id, step_index):
        if jammer_id not in self.jammer_paths:
            raise ValueError(f"Jammer '{jammer_id}' not found")
        path = self.jammer_paths[jammer_id]
        if step_index >= len(path):
            return None
        return path[step_index]
    
    def get_all_positions_at_step(self, step_index):
        positions = {}
        for jammer_id, path in self.jammer_paths.items():
            if step_index < len(path):
                positions[jammer_id] = path[step_index]
        return positions
    
    def update_scene_transmitters(self, step_index):
        positions = self.get_all_positions_at_step(step_index)
        for jammer_id, position in positions.items():
            try:
                tx = self.scene.get(jammer_id)
                tx.position = position
            except:
                print(f"Warning: Transmitter '{jammer_id}' not found in scene")
    
    def get_max_path_length(self):
        if not self.jammer_paths:
            return 0
        return max(len(path) for path in self.jammer_paths.values())
    
    def create_path_matrix(self, padding_mode='pad_end'):
        if not self.jammer_paths:
            raise ValueError("No jammer paths found")
        
        max_steps = self.get_max_path_length()
        path_lengths = {jid: len(path) for jid, path in self.jammer_paths.items()}
        all_equal = len(set(path_lengths.values())) == 1
        
        if padding_mode == 'error' and not all_equal:
            raise ValueError(f"Path lengths are not equal: {path_lengths}. Use different padding_mode or ensure equal lengths.")
        
        if padding_mode == 'none':
            return self.jammer_paths, max_steps
        
        padded_paths = {}
        for jammer_id, path in self.jammer_paths.items():
            path_len = len(path)
            if path_len == max_steps:
                padded_paths[jammer_id] = path
            else:
                pad_amount = max_steps - path_len
                if padding_mode == 'pad_end':
                    last_pos = path[-1]
                    padding = np.tile(last_pos, (pad_amount, 1))
                    padded_path = np.vstack([path, padding])
                elif padding_mode == 'pad_start':
                    first_pos = path[0]
                    padding = np.tile(first_pos, (pad_amount, 1))
                    padded_path = np.vstack([padding, path])
                else:
                    raise ValueError(f"Unknown padding_mode: {padding_mode}")
                padded_paths[jammer_id] = padded_path
                print(f"Padded '{jammer_id}' from {path_len} to {max_steps} steps (mode: {padding_mode})")
        
        return padded_paths, max_steps
