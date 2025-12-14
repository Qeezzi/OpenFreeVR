using UnityEngine;

public class CreateHandPoints : MonoBehaviour
{
    void Start()
    {
        Color[] colors = {
            Color.white,
            Color.red, Color.red, Color.red, Color.red,
            Color.green, Color.green, Color.green, Color.green,
            Color.blue, Color.blue, Color.blue, Color.blue,
            Color.yellow, Color.yellow, Color.yellow, Color.yellow,
            Color.cyan, Color.cyan, Color.cyan, Color.cyan
        };

        for (int i = 0; i < 21; i++)
        {
            GameObject s = GameObject.CreatePrimitive(PrimitiveType.Sphere);
            s.name = "Point" + i;
            s.transform.SetParent(transform);
            s.transform.localPosition = Vector3.zero;
            s.transform.localScale = Vector3.one * 0.025f;
            var r = s.GetComponent<Renderer>();
            r.material = new Material(Shader.Find("Standard"));
            r.material.color = colors[i];
        }
        Destroy(this);
    }
}
