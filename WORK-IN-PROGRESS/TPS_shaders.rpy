# custom glow/gradient shader developed by me based on original work by Stella@MaKeVisualNovels
# https://makevisualnovels.itch.io/
#
# Concept behind this shader is:
# - text represent a character's conscious thought processes
# - the glow is the character's own feelings "seeping through" - it's the way the speak, the way a pause lasts longer than it should, etc.
# - glow should be given the possibility to bleed into the text - and vice-versa. The obvious meaning is, the subconscious invading 
# a character's conscious processes; or, consciousness actively restraining the subconscious.
# - a single shader performing all of the above allows for seamless transitions between states, allowing me to use my TPS's transition
# "engine" to perform smooth transitions between a shader setting and another (including a state with no shader at all!). One does not
# gets from sadness to happiness in just a couple dialogue lines after all!
#
# Each pixel's color is a convolution of the the color of pixels surrounding it within a circle of u__glow_radius. It follows that a pixel
# very close to glyphs (ie. opaque or nearly totally opaque pixels) will be more opaque than a pixel located far from the text.
# To easen the computational burden, sampling within the convolution radius does not pick each and every pixel but rather it follows below
# sampling logic:
# - sampling is capped at 200 samples maximum (actually is 201 since index goes from 0 to 200 _included_)
# - sampling logic considers polar coordinates which are then converted to Cartesian using simple trigonometry
# - pixel are distributed so that the sampling density remains constant. This means sampling distance from center follows a rule
# proportional to sqrt(r)
# - sampling azimuth follows a golden spiral pattern (that is, the golden ratio is used to determine the sample's azimuth)
# The result is a sampling pattern that ends up looking a bit like a spiral galaxy
#
# The text model's alpha channel is used as a basis to create an alpha mask for the glow. Each pixel's alpha channel is weighed
# against the distance from the glyphs using a Gaussian distribution function:
#              pixel_color.alpha ∼ exp(-r^2/(2*sigma^2))
# hence the overall intensity of the glow can be estimated (by integrating the Gaussian function in the [-inf;+inf] range) as:
#               E ∼ u__glow_color.a * 2 * pi * sigma^2
# where u__glow_color.a is the glow color's alpha channel and sigma is the curve's standard deviation and can be set by user.
#
# The glow theoretically exists in the text region too (ie. on the glyphs themselves). The dedicated u__glow_bleeds_into_text parameter
# allows user to decide how much of the glow color will bleed into text - it basically acts as a multiplier to the glow's alpha channel.
# NOTE THAT THIS CURRENTLY RESULTS IN ADDITIVE COLORING as this shader works in the RGB space and RGB is inherently additive ie.
# #ffff00 (yellow) + #ff0000 (red) = #ffff00 (yellow) and not orange!
# future versions of the shader may include a conversion to HSV space and hue-based mixing so that yellow+red=orange
#
# The shader also gives the possibility to have the text color to bleed into the glow. The dedicated u__text_bleeds_into_glow parameter
# allows user to decide how much of the color will bleed into text - the shader basically creates a blurry version of the text and
# then multiplies its alpha channel by u__text_bleeds_into_glow. THE SAME WARNING ABOUT RGB SPACE BEING ADDITIVE APPLIES HERE TOO SO
# #00ffff (cyan) + #ff0000 (red) = #ffffff (white) instead of whatever you might expect from this mix!

# Deep they delved us, fair they wrought us, high they builded us; but they are gone. They are gone
init -1500 python:


# One Shader To Rule Them All,
# One Shader To Find Them,
# One Shader To Bring Them All
# And In The Fragment Bind Them.
    renpy.register_textshader(
        "TheOneShader",
# Two Uniforms for the Glow-kings under the sky,
# Four for the Gradient-lords in their halls of stone,
# Seven for Gaussians, doomed to die,
# One for the Dark Lord on his dark throne
# In the Land of Blending where the Shaders lie.
        variables="""
        uniform float u__text_f1;
        uniform float u__text_f2;
        uniform float u__glow_f1;
        uniform float u__glow_f2;
        uniform vec4 u__text_col1;
        uniform vec4 u__text_col2;
        uniform vec4 u__glow_col1; 
        uniform vec4 u__glow_col2;
        uniform float u__text_bleeds_into_glow;
        uniform float u__text_sigma;
        uniform float u__glow_sigma;
        uniform float u__text_radius;
        uniform float u__glow_radius;
        uniform float u__glow_bleeds_into_text;
        uniform vec2 u_model_size;   
        varying vec2 v__uv;          
        attribute vec2 a_tex_coord;  
        """,

# Where now the coder and the debugger? Where is the bug that was blowing?
# Where is the pixel and the vertex, and the bright texture flowing?
        vertex_300="""
        v__uv = a_tex_coord;
        """,


        fragment_300="""
            float text_t = 0.5 + 0.35 * sin(v__uv.x * u__text_f1) + 0.22 * sin(v__uv.x * u__text_f2 + 0.7854);
            float glow_t = 0.49 + 0.38 * sin(v__uv.x * u__glow_f1) - 0.15 * sin(v__uv.x * u__glow_f2 - 0.7854);
            text_t = clamp(text_t, 0.0, 1.0);
            glow_t = clamp(glow_t, 0.0, 1.0);

            vec4 text_gradient;
            vec4 text_color;
            vec4 glow_gradient;
            vec4 text_blur_gradient;
            float text_mask = texture2D(tex0,v__uv).a;

            /*****************************************/
            /* TEXT COLOR                            */
            /*****************************************/
// It came to me. My own. My love. My... gradienttttttt...
            bool is_text_gradient = (u__text_col2.a) > 0.0 && (distance(u__text_col1,u__text_col2) > 0.001);

            if (is_text_gradient) {
                text_gradient = mix(u__text_col1, u__text_col2, text_t);
                text_color = vec4(text_gradient.rgb,text_gradient.a * text_mask);
            }
// I am a servant of the secret fire, wielder of the flame of Text Color. You cannot pass!
            else {
                text_gradient = texture2D(tex0, v__uv);
                text_color = vec4(text_gradient.rgb,text_gradient.a);
            }

            /*****************************************/
            /* GLOW                                  */
            /*****************************************/
            bool is_glow_gradient = (u__glow_col2.a) > 0.0 && (distance(u__glow_col1,u__glow_col2) > 0.001);
            if (is_glow_gradient) {
                glow_gradient = mix(u__glow_col1, u__glow_col2,  glow_t);
                }
            else {
                glow_gradient = u__glow_col1;
                }

            vec4 text_blur_color = vec4(0.0);
            vec4 glow_color = vec4(0.0);
            float global_weight_text = 0.0;
            float global_weight_glow = 0.0;

// The Sampling is Shut. It Was Made by Those Who Are Dead, and The Dead Keep It, Until The Time Comes
            float samples_cap = 200.0;
            float glow_required_samples = min(3.14159 * u__glow_radius * u__glow_radius,samples_cap);
            float text_required_samples = min(3.14159 * u__text_radius * u__text_radius,samples_cap);

            for (float i = 0.0; i < glow_required_samples; i++) {
                float u_g = i / glow_required_samples;
                float r_g = u__glow_radius * sqrt(u_g);

// Not all those who wander are lost
                float v_g = fract(i/1.618034);
                float theta_g = 2.0 * 3.141593 * v_g;
                vec2 offset_g = vec2(r_g * cos(theta_g), r_g * sin(theta_g)) / u_model_size;
                float sample_mask = texture2D(tex0,v__uv + offset_g).a;

// Even Gaussian must pass
                float local_weight_glow = exp(-r_g*r_g / (2*u__glow_sigma*u__glow_sigma));
                vec4 sample_glow = vec4(glow_gradient.rgb,glow_gradient.a);
                glow_color += sample_glow * sample_mask * local_weight_glow;
                global_weight_glow += local_weight_glow;
            }
          
            /*****************************************/
            /* BLOOM                                 */
            /*****************************************/
//  I was there, the day the strength of text gradient failed
            text_blur_gradient = vec4(text_gradient.rgb,text_color.a * u__text_bleeds_into_glow);

            if (u__text_bleeds_into_glow > 0.0) {
// One does not simply walk into bloom
                for (float j = 0.0; j < text_required_samples; j++) {
                    float u_t = j / text_required_samples;
                    float r_t = u__text_radius * sqrt(u_t);
                    float v_t = fract(j/1.618034);
                    float theta_t = 2.0 * 3.141593 * v_t;
                    vec2 offset_t = vec2(r_t * cos(theta_t), r_t * sin(theta_t)) / u_model_size;
                    float sample_mask = texture2D(tex0,v__uv + offset_t).a;
                    float local_weight_text = exp(-r_t*r_t / (2*u__text_sigma*u__text_sigma));
                    vec4 sample_blur = vec4(text_blur_gradient.rgb,text_blur_gradient.a);
                    text_blur_color += sample_blur * sample_mask * local_weight_text;
                    global_weight_text += local_weight_text;
                }
            }

// All we have to decide is what to do with the glow that is given us.
            glow_color /= max(global_weight_glow,0.001);
            text_blur_color /= max(global_weight_text,0.001);
            float center_mask = texture2D(tex0,v__uv).a;

// I will not say: do not weep; for not all bleedings are an evil
            float bleeding = mix(pow(1.0 - center_mask,2.0),1.0,u__glow_bleeds_into_text);
            glow_color *= bleeding;

// The Fragment-That-Was-Broken shall be reforged
            vec3 final_color_rgb = text_color.rgb;
            final_color_rgb = mix(final_color_rgb,glow_color.rgb*5.0,glow_color.a);
            final_color_rgb = mix(final_color_rgb,text_blur_color.rgb,text_blur_color.a);

            float final_color_alpha = clamp(text_color.a + glow_color.a + text_blur_color.a,0.0,1.0);
            gl_FragColor = glow_color; //vec4(final_color_rgb,final_color_alpha);
            """,

# Concerning defaults
        u__text_f1 = 17.0,
        u__text_f2 = 57.0,
        u__glow_f1 = 9.0,
        u__glow_f2 = 79.0,
        u__text_col1 = "#fafcff",
        u__text_col2 = "#00000000",
        u__glow_col1 = "#b9d8f790",
        u__glow_col2 = "#00000000",
        u__text_bleeds_into_glow = 0.0,
        u__text_sigma = 4.5,
        u__glow_sigma = 3.0,
        u__text_radius = 6.0,
        u__glow_radius = 9.0,
        u__glow_bleeds_into_text = 0.4
)

##########################################################################################################################
##########################################################################################################################
##########################################################################################################################
#
# below shaders are a WIP project - they basically are a "underpowered" version of TheOneShader with limited capabilities
# and a much more lenient learning curve (ie. they don't ask user to delve into eldritch formulations and the darkest recesses
# of an engineer's mind - they just ask for a color and two parameter, and then you're good to go)


# custom glow shader developed by me based on original Glow shader by Stella@MaKeVisualNovels
# https://makevisualnovels.itch.io/
# original glow calculates actual glow color as a multiplication between text color and glow color. This modified glow
# generates a glow whose color is independent of the text color (the opposite does not hold, see below).
# Concept behind this glow is:
# - text represent a character's conscious thought processes
# - the glow is the character's own feelings "tainting" consciousness
# - the glow bleeding into the text has the obvious implication of consciousness being growingly driven by subconscious processes
#
# The text model's alpha channel is used as a basis to create an alpha mask for the glow. Each pixel's alpha channel is weighed
# against the distance from the glyphs using a Gaussian distribution function:
#              pixel_color.alpha ∼ exp(-r^2/(2*sigma^2))
# this means, we control the total energy and its density. The total energy (which can be calculated by integrating the
# Gaussian function in the [-inf;+inf] range) always is directly proportional to sigma^2:
#                E ∼ 2 * pi * sigma^2
#
# The glow theoretically exists in the text region too (ie. on the glyphs themselves). The dedicated u__glow_bleeds_into_text parameter allows
# user to decide how much of the glow color will bleed into text.
#
# args:
#        u__glow_color -> color of the glow halo. Strongly recommended to be input as RGBA (ie. #rrggbbaa) as the color's alpha
#                         channel affects the halo's perceived intensity
#        u__glow_sigma -> standard deviation of the Gaussian curve used as weight in the calculation of the glow's alpha channel
#        u__glow_radius -> the radius of the sampling circumference. Each pixel will get a glow intensity that depends on the alpha
#                          of the pixels surrounding it within a circumference of radius u__glow_radius
#        u__glow_bleeds_into_text -> parameter establishing how much of the glow bleeds into text. A bleed of 0.5 means, resulting text color will be
#                         the sum of the text's own color and the glow's rgba vector multiplied by 0.5
#
# usage:
#        {shader=pure_glow:u__glow_color=#rrggbbaa:u__glow_sigma=FLOAT:u__glow_radius=FLOAT:u__glow_bleeds_into_text=FLOAT}
#        not adding a dedicated Ren'Py tag because of the way I use shaders within my own TPS system
    renpy.register_textshader(
        "pure_glow",
        variables="""
        uniform vec4 u__glow_color;
        uniform float u__glow_sigma;
        uniform float u__glow_radius;  
        uniform float u__glow_bleeds_into_text;
        uniform vec2 u_model_size;
        varying vec2 v__uv;             
        attribute vec2 a_tex_coord;     
        """,
    
        vertex_300="""
        
        v__uv = a_tex_coord;
        """,
    
        fragment_300="""
        vec4 text_color = texture2D(tex0,v__uv);
        vec4 glow_color = vec4(0.0);
        float global_weight = 0.0;
    
// capping the total number of samples so that calculations won't explode for larger radiuses
// at the same time I don't want to take a huge number of samples with smaller radiuses
// capping will occur when u__glow_radius > 8
        float samples_cap = 200.0;

        float required_samples = min(3.14159 * u__glow_radius * u__glow_radius,samples_cap);
  
// loop to calculate the color intensity of pixel at location [r,theta] on polar coordinates
// r grows in such a way that's proportional to the *area* ie. when i = 0.5 r is the radius that
// encompassess half the sampling area; theta uses the golden ratio to approximate a spiral
// this way sampling points are distributed evenly over the entire sampling area
        for (float i = 0.0; i <= required_samples; i++) {
            float u = i / required_samples;
            float r = u__glow_radius * sqrt(u);
            float v = fract(i/1.618034);
            float theta = 2.0 * 3.141593 * v;
            vec2 offset = vec2(r * cos(theta), r * sin(theta)) / u_model_size;
            float sample_mask = texture2D(tex0,v__uv + offset).a;
            float local_weight = exp(-r*r / (2*u__glow_sigma*u__glow_sigma));
            vec4 sample_glow = vec4(u__glow_color.rgb,u__glow_color.a);
            glow_color += sample_glow * sample_mask * local_weight;
            global_weight += local_weight;
        }
    
        glow_color /= max(global_weight,0.001);
    
        float center_mask = texture2D(tex0,v__uv).a;
        float bleeding = mix(pow(1.0 - center_mask,2.0),1.0,u__glow_bleeds_into_text);
        glow_color *= bleeding;
        gl_FragColor = text_color + glow_color;
        """,
    
        u__glow_color="#ff0000",    # Default glow color (White)
        u__glow_sigma=3.0,          # Default standard deviation for weight curve
        u__glow_radius=8.0,         # Sampling radius
        u__glow_bleeds_into_text=0.5,          # Default bleed
)

# another custom glow shader developed by me based on original Glow shader by Stella@MaKeVisualNovels
# https://makevisualnovels.itch.io/
# original glow calculates actual glow color as a multiplication between text color and glow color. This modified glow
# generates a glow that's the summation of a text-based glow (ie. glow color is the same as text color) and that of the actual glow

# Calculation logic is identical to that of pure_glow shader.
# Concept behind this glow is the opposite of pure_glow: here it's consciousness that bleeds into the subconscious providing restraint
#
# First I calculate the glow component of a pixel's color, using the same pattern I already use with the pure_glow.
# Then the contribution due to text's own "bloom" is added following the same math and logic, but with different [sigma,radius,alpha] (ie.
# different intensity and spread).
# A pixel very close to the glyphs will receive a lot of contribution from fully opaque or nearly fully opaque pixels and its color will be
# a mix of text and glow colors. A pixel far from the text will be mostly the same color as u__glow_color but very dim.
# One could tinker with the glow and text sigma parameters to have a more "evenly distributed" glow that spreads past a more concentrated
# text bloom.
# No bleed is considered as this shader is supposed to show a text that blurs into its own glow and not vice-versa.
#
# args:
#        u__glow_color -> color of the glow halo. Strongly recommended to be input as RGBA (ie. #rrggbbaa) as the color's alpha
#                         channel affects the halo's perceived intensity
#        u__text_bleeds_into_glow -> alpha value that gets applied to text glow. Text will use a RGBA (ie. #rrggbbaa) using the text color's
#                                  rgb channels and with the alpha channel equal to u__text_bleeds_into_glow
#        u__glow_sigma -> standard deviation of the Gaussian curve used as weight in the calculation of the glow's alpha channel
#        u__glow_radius -> the radius of the sampling circumference. Each pixel will get a glow intensity that depends on the alpha
#                          of the pixels surrounding it within a circumference of radius u__glow_radius
#        u__text_sigma -> standard deviation of the Gaussian curve used as weight in the calculation of the text's alpha channel
#        u__text_radius -> the radius of the sampling circumference. Each pixel will get a text intensity that depends on the alpha
#                          of the pixels surrounding it within a circumference of radius u_text_radius
#
# usage:
#        {shader=pure_glow:u__glow_color=#rrggbbaa:u__text_bleeds_into_glow=FLOAT:u__text_sigma=FLOAT:u__glow_sigma=FLOAT:u__text_radius=FLOAT:u__glow_radius=FLOAT}
#        not adding a dedicated Ren'Py tag because of the way I use shaders within my own TPS system

    renpy.register_textshader(
        "mixed_glow",
        variables="""
        uniform vec4 u__glow_color;
        uniform float u__text_bleeds_into_glow;
        uniform float u__text_sigma;
        uniform float u__glow_sigma;
        uniform float u__text_radius;
        uniform float u__glow_radius;
        uniform vec2 u_model_size;
        varying vec2 v__uv;             
        attribute vec2 a_tex_coord;     
        """,
    
        vertex_300="""
        
        v__uv = a_tex_coord;
        """,
    
        fragment_300="""
        vec4 base_text = texture2D(tex0,v__uv);
        vec4 text_color = vec4(base_text.rgb, base_text.a * u__text_bleeds_into_glow);
        vec4 text_blur_color = vec4(0.0);
        vec4 glow_color = vec4(0.0);
        float global_weight_text = 0.0;
        float global_weight_glow = 0.0;
  
// capping the total number of samples so that calculations won't explode for larger radiuses
// at the same time I don't want to take a huge number of samples with smaller radiuses
// capping will occur when u__glow_radius > 8;
        float samples_cap = 200.0;             
                             
        float glow_required_samples = min(3.14159 * u__glow_radius * u__glow_radius,samples_cap);
        float text_required_samples = min(3.14159 * u__text_radius * u__text_radius,samples_cap);
  
// loop to calculate the color intensity of pixel at location [r,theta] on polar coordinates
// r grows in such a way that's proportional to the *area* ie. when i = 0.5 r is the radius that
// encompassess half the sampling area not just "half u__glow_radius"; theta uses the golden ratio
// to approximate a spiral
// this way sampling points are distributed more evenly over the entire sampling area
        for (float i = 0.0; i < glow_required_samples; i++) {
            float u_g = i / glow_required_samples;
            float r_g = u__glow_radius * sqrt(u_g);
            float v_g = fract(i/1.618034);
            float theta_g = 2.0 * 3.141593 * v_g;
            vec2 offset_g = vec2(r_g * cos(theta_g), r_g * sin(theta_g)) / u_model_size;
            float sample_mask = texture2D(tex0,v__uv + offset_g).a;
            float local_weight_glow = exp(-r_g*r_g / (2*u__glow_sigma*u__glow_sigma));
            vec4 sample_glow = vec4(u__glow_color.rgb,text_color.a);
            glow_color += sample_glow * sample_mask * local_weight_glow;
            global_weight_glow += local_weight_glow;
        }
  
        for (float j = 0.0; j < text_required_samples; j++) {
            float u_t = j / text_required_samples;
            float r_t = u__text_radius * sqrt(u_t);
            float v_t = fract(j/1.618034);
            float theta_t = 2.0 * 3.141593 * v_t;
            vec2 offset_t = vec2(r_t * cos(theta_t), r_t * sin(theta_t)) / u_model_size;
            float sample_mask = texture2D(tex0,v__uv + offset_t).a;
            float local_weight_text = exp(-r_t*r_t / (2*u__text_sigma*u__text_sigma));
            vec4 sample_blur = vec4(text_color.rgb,text_color.a);
            text_blur_color += sample_blur * sample_mask * local_weight_text;
            global_weight_text += local_weight_text;
        }
    
        glow_color /= max(global_weight_glow,0.001);
        text_blur_color /= max(global_weight_text,0.001);
        float center_mask = texture2D(tex0,v__uv).a;
        float bleeding = mix(pow(1.0 - center_mask,2.0),1.0,0.0);
        glow_color *= bleeding;
        gl_FragColor = base_color + text_blur_color + glow_color;
        """,
  
        u__glow_color="#ff0000",          # Default glow color (White)
        u__glow_sigma=3.0,                # Default standard deviation for weight curve
        u__glow_radius=8.0,               # Sampling radius
        u__text_sigma=4.0,                # Default standard deviation for weight curve
        u__text_radius=4.0,               # Sampling radius
        u__text_bleeds_into_glow=0.5        # corresponds to an alfa 0x80
    )
