import scipy as sci

def lowpass_filter(data, cutoff, order=4):
    
    """
    Applies a low-pass Butterworth filter to the data, where cutoff is
    a normalized value between 0 and 1 (relative to the signal's length).
    
    Parameters:
        data (array): Input signal to be filtered.
        cutoff (float): Normalized cutoff for the low-pass filter (0 to 1).
        order (int): The order of the filter (default is 4).
        
    Returns:
        filtered_data (array): Filtered signal.
    """
    # Define the Nyquist rate based on the length of the data (signal's total time span)
    nyquist = 0.5 * len(data)  # Use the length of the data instead of a frequency-based concept
    
    # Design the Butterworth filter based on normalized cutoff
    normal_cutoff = cutoff  # Cutoff is directly used as a normalized value
    
    # Design the Butterworth filter
    b, a = sci.signal.butter(order, normal_cutoff, btype='low', analog=False)
    
    # Apply the filter to the data
    filtered_data = sci.signal.filtfilt(b, a, data)

    return filtered_data