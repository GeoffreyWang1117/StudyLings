#version 450

// 全屏四边形顶点着色器
// 无需顶点缓冲，直接在着色器中生成顶点

// 输出到片段着色器
layout(location = 0) out vec2 fragTexCoord;

void main() {
    // 使用 gl_VertexIndex 生成全屏三角形
    // 顶点索引: 0, 1, 2 生成一个覆盖整个屏幕的三角形
    //
    //   1
    //   |\
    //   | \
    //   |  \
    //   |   \
    //   |----2
    //   0
    //
    // 位置:
    // 0: (-1, -1)  左下
    // 1: (-1,  3)  左上 (超出屏幕)
    // 2: ( 3, -1)  右下 (超出屏幕)

    vec2 positions[3] = vec2[](
        vec2(-1.0, -1.0),
        vec2(-1.0,  3.0),
        vec2( 3.0, -1.0)
    );

    vec2 texCoords[3] = vec2[](
        vec2(0.0, 0.0),
        vec2(0.0, 2.0),
        vec2(2.0, 0.0)
    );

    gl_Position = vec4(positions[gl_VertexIndex], 0.0, 1.0);
    fragTexCoord = texCoords[gl_VertexIndex];
}
