Lower
=====

This folder has files for testing Make Lowercase functionality

####Test file: lower.txt

0. UPLOAD lower.txt

1. SCRUB: 
    - deactivate Remove all Punct
    - Make Lowercase
    - Remove Digits (optional)
    
Results:
- file content: upper -> lower case thorn þ þ eth ð ð ƥ ƥ ƨ ƨ m m ï ï ā ā œ œ ƃ ƃ ǟ ǟ ǿ ǿ ɣ ɣ e e ψ ψ ή ή z z

####Test file: lowerTest1.txt

0. UPLOAD lowerTest1.txt

1. SCRUB: 
    - deactivate Remove all Punct
    - Make Lowercase
    - Remove Digits (optional)
    
Results:
- file content: uppercase: a æ b c d ð e f ᵹ/g h i l m n o p r s t þ u ƿ/w x y
                lowercase: a æ b c d ð e f ᵹ/g h i l m n o p r s/ſ t þ u ƿ/w x y

####Test file: greekTest.txt

0. UPLOAD greekTest.txt

1. SCRUB: 
    - deactivate Remove all Punct
    - Make Lowercase
    - Remove Digits (optional)
    
Results:
- file content: uppercase: α β γ δ ε ζ η θ ι κ λ μ ν ξ ο π ρ σ τ υ φ χ ψ ω 
                lowercase: α β γ δ ε ζ η θ ι κ λ μ ν ξ ο π ρ ς/σ τ υ φ χ ψ ω

####Test file: spanishTest.txt

0. UPLOAD spanishTest.txt

1. SCRUB: 
    - Remove all Punct (optional)
    - Make Lowercase
    - Remove Digits (optional)
    
Results:
- file content: a a b b c c d d e e f f g g h h i i j j k k l l ll ll m m n n ñ ñ o o p p q q r r s s t t u u v v w w x x y y z z 
