#[cfg(target_arch = "x86_64")]
use core::arch::x86_64::*;
// before compiling, ensure you have: RUSTFLAGS="-C target-feature=+f16c" cargo run
fn main() {
    unsafe {
        let original: f32 = 3.14159;

        let vector_f16 = _mm_cvtps_ph(_mm_set_ss(original), 0); // _MM_FROUND_TO_NEAREST_INT |_MM_FROUND_NO_EXC, 0 for rounding mode

        let memory: u16 = _mm_extract_epi16(vector_f16, 0) as u16;

        println!("16 bits float: {}", memory);
        println!("Binary: {:016b}", memory);

        let f32_vector = _mm_cvtph_ps(_mm_set1_epi16(memory as i16));
        
        let mut number: f32 = 0.0;
        _mm_store_ss(&mut number, f32_vector);
    }
}