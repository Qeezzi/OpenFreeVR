using UnityEngine;
using System.Net;
using System.Net.Sockets;

public class HandUDPReceiver : MonoBehaviour
{
    public Transform[] points; // назначьте 21 точку (Point0..Point20)
    public GameObject cube;    // опционально — для визуальной реакции

    private UdpClient client;

    void Start()
    {
        if (points == null || points.Length != 21)
        {
            Debug.LogError("❌ Нужно ровно 21 Transform в массиве points.");
            return;
        }
        try
        {
            client = new UdpClient(5005);
            client.Client.ReceiveTimeout = 10;
            Debug.Log("📡 UDP слушает 127.0.0.1:5005");
        }
        catch (System.Exception e)
        {
            Debug.LogError("UDP error: " + e.Message);
        }
    }

    void Update()
    {
        if (client == null) return;
        try
        {
            IPEndPoint ep = null;
            byte[] data = client.Receive(ref ep);
            if (data.Length != 256) return;

            float detected = System.BitConverter.ToSingle(data, 0);
            if (detected < 0.5f) return;

            for (int i = 0; i < 21; i++)
            {
                int o = 4 + i * 12;
                float x = System.BitConverter.ToSingle(data, o + 0);
                float y = System.BitConverter.ToSingle(data, o + 4);
                float z = System.BitConverter.ToSingle(data, o + 8);
                points[i].position = new Vector3(x, y, 1.5f + z);
            }

            if (cube != null)
            {
                float dist = Vector3.Distance(points[8].position, cube.transform.position);
                bool touching = dist < 0.15f;
                var r = cube.GetComponent<Renderer>();
                if (r != null) r.material.color = touching ? Color.green : Color.white;
            }
        }
        catch { }
    }

    void OnDestroy()
    {
        try { client?.Close(); } catch {}
    }
}
